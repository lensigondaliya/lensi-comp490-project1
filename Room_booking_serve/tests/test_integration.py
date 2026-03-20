import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import pytest

from skills import (
    book_room,
    cancel_booking,
    get_available_rooms,
    get_my_bookings,
    login_access_token,
)


def _require_env(name: str) -> str:
    val = os.getenv(name)
    if not val:
        pytest.skip(f"Missing environment variable {name}")
    return val


def _iso_utc(dt: datetime) -> str:
    
    return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _normalize_bookings(raw: Any) -> List[Dict[str, Any]]:
    if isinstance(raw, list):
        return raw
    if isinstance(raw, dict) and isinstance(raw.get("results"), list):
        return raw["results"]
    if isinstance(raw, dict) and isinstance(raw.get("data"), list):
        return raw["data"]
    if isinstance(raw, dict) and isinstance(raw.get("bookings"), list):
        return raw["bookings"]
    return []


def _room_id_from_room(room: Dict[str, Any]) -> Optional[int]:
    for k in ("id", "room_id", "pk"):
        v = room.get(k)
        if isinstance(v, int):
            return v
    return None


def _booking_matches(b: Dict[str, Any], room_id: int, start_time: str, end_time: str) -> bool:
    
    mr = b.get("meeting_room") or {}
    bid = mr.get("id") or mr.get("room_id") or b.get("room_id") or b.get("meeting_room_id")
    if bid != room_id:
        return False

    bs = str(b.get("start_time", ""))
    be = str(b.get("end_time", ""))

    return (start_time[:16] in bs) and (end_time[:16] in be)


def _booking_id(b: Dict[str, Any]) -> Optional[int]:
    
    for k in ("id", "booking_id", "pk"):
        v = b.get(k)
        if isinstance(v, int):
            return v
    return None


@pytest.mark.integration
def test_sprint3_end_to_end_book_then_cancel():
    _require_env("SERVER_URL")
    email = _require_env("EMAIL")
    password = _require_env("PASSWORD")

    # 1) login
    token = login_access_token(email, password)
    assert isinstance(token, str) and len(token) > 10

    # 2) choose a start/end time in near future
    now = datetime.now(timezone.utc)
    start_dt = (now + timedelta(minutes=15)).replace(second=0, microsecond=0)
    end_dt = start_dt + timedelta(minutes=15)
    start_time = _iso_utc(start_dt)
    end_time = _iso_utc(end_dt)

    # 3) available rooms
    rooms = get_available_rooms(token, start_time=start_time, end_time=end_time)
    assert isinstance(rooms, list) and len(rooms) > 0

    room_id = _room_id_from_room(rooms[0])
    assert isinstance(room_id, int)

    # 4) book
    book_resp = book_room(token, room_id, start_time, end_time, no_of_persons=1)
    assert book_resp.get("ok") is True, f"Booking failed: {book_resp}"

    # 5) find booking id by refreshing my-bookings
    raw = get_my_bookings(token)
    bookings = _normalize_bookings(raw)
    assert bookings, "No bookings returned after booking"

    match = None
    for b in bookings:
        if _booking_matches(b, room_id, start_time, end_time):
            match = b
            break

    assert match is not None, f"Could not find newly created booking in my-bookings. start={start_time} end={end_time}"

    bid = _booking_id(match)
    assert isinstance(bid, int), f"Found booking but could not extract booking id: {match}"

    # 6) cancel
    cancel_resp = cancel_booking(token, bid)
    assert cancel_resp.get("ok") is True, f"Cancel failed: {cancel_resp}"