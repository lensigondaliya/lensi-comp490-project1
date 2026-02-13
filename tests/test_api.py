import os
from datetime import datetime, timedelta

import pytest

from skills import book_room, get_available_rooms, login_access_token


EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


def fmt(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %I:%M %p")


@pytest.mark.skipif(not EMAIL or not PASSWORD, reason="EMAIL/PASSWORD env vars not set")
def test_login_get_token():
    token = login_access_token(EMAIL, PASSWORD)
    assert isinstance(token, str)
    assert len(token) > 10


@pytest.mark.skipif(not EMAIL or not PASSWORD, reason="EMAIL/PASSWORD env vars not set")
def test_available_rooms_returns_list():
    token = login_access_token(EMAIL, PASSWORD)
    start_dt = datetime(2026, 2, 20, 18, 0)  # 6:00 PM
    end_dt = start_dt + timedelta(minutes=15)
    rooms = get_available_rooms(token, fmt(start_dt), fmt(end_dt))
    assert isinstance(rooms, list)


@pytest.mark.skipif(not EMAIL or not PASSWORD, reason="EMAIL/PASSWORD env vars not set")
def test_booking_then_double_booking_fails():
    token = login_access_token(EMAIL, PASSWORD)

    # window (change these numbers if it skips)
    start_dt = datetime(2026, 2, 20, 8, 0)

    end_dt = start_dt + timedelta(minutes=15)
    start_time = fmt(start_dt)
    end_time = fmt(end_dt)

    rooms = get_available_rooms(token, start_time, end_time)
    print("ROOMS:", rooms)

    if not rooms:
        pytest.skip("No available rooms for that window; try another fixed time.")

    room_id = rooms[0]["id"]

    # first booking should succeed
    first = book_room(token, room_id, start_time, end_time, no_of_persons=1)
    assert first["ok"] is True

    # second booking same room same time should fail
    second = book_room(token, room_id, start_time, end_time, no_of_persons=1)
    assert second["ok"] is False
