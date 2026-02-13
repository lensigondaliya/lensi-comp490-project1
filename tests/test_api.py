import os
from datetime import datetime, timedelta

import pytest

from skills import book_room, get_available_rooms, login_access_token

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")


def fmt(dt: datetime) -> str:
    # server format: "YYYY-MM-DD HH:MM AM/PM"
    return dt.strftime("%Y-%m-%d %I:%M %p")


def future_window(minutes: int = 15):
    """Return (start_time, end_time) strings for a window 1 hour from now."""
    start_dt = datetime.now() + timedelta(hours=1)
    start_dt = start_dt.replace(second=0, microsecond=0)
    end_dt = start_dt + timedelta(minutes=minutes)
    return fmt(start_dt), fmt(end_dt)


@pytest.mark.skipif(not EMAIL or not PASSWORD, reason="EMAIL/PASSWORD env vars not set")
def test_login_get_token():
    token = login_access_token(EMAIL, PASSWORD)
    assert isinstance(token, str)
    assert len(token) > 10


@pytest.mark.skipif(not EMAIL or not PASSWORD, reason="EMAIL/PASSWORD env vars not set")
def test_available_rooms_returns_list():
    token = login_access_token(EMAIL, PASSWORD)

    start_time, end_time = future_window(15)
    rooms = get_available_rooms(token, start_time=start_time, end_time=end_time)

    assert isinstance(rooms, list)
    assert len(rooms) > 0  # make sure we actually got rooms


@pytest.mark.skipif(not EMAIL or not PASSWORD, reason="EMAIL/PASSWORD env vars not set")
def test_booking_then_double_booking_fails():
    token = login_access_token(EMAIL, PASSWORD)

    start_time, end_time = future_window(15)
    rooms = get_available_rooms(token, start_time=start_time, end_time=end_time)

    if not rooms:
        pytest.skip("No available rooms for that time window; try rerun.")

    room_id = rooms[0]["id"]

    # first booking should succeed
    first = book_room(token, room_id, start_time, end_time, no_of_persons=1)
    assert first["ok"] is True

    # second booking same room same time should fail
    second = book_room(token, room_id, start_time, end_time, no_of_persons=1)
    assert second["ok"] is False
