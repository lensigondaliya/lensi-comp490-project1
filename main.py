import os
from datetime import datetime, timedelta

from skills import (
    book_room,
    get_available_rooms,
    get_my_bookings,
    list_rooms,
    login_access_token,
    cancel_booking,
)

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

if not EMAIL or not PASSWORD:
    raise SystemExit("Missing EMAIL or PASSWORD in environment variables.")

# Time format required by server: "YYYY-MM-DD HH:MM AM/PM"
def fmt(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %I:%M %p")


def main():
    token = login_access_token(EMAIL, PASSWORD)
    print("✅ Logged in, token received.\n")

    # pick a time window (15 min)
    now = datetime.now()
    start_dt = now + timedelta(hours=1)          # 1 hour from now
    start_dt = start_dt.replace(second=0, microsecond=0)
    end_dt = start_dt + timedelta(minutes=15)

    start_time = fmt(start_dt)
    end_time = fmt(end_dt)


    print("Time window:", start_time, "->", end_time, "\n")

    # Call list rooms 
    rooms_all = list_rooms(token)
    print(f"✅ Total rooms returned: {len(rooms_all)}\n")

    # Get available rooms for the window
    rooms = get_available_rooms(token, start_time=start_time, end_time=end_time)
    print(f"✅ Available rooms: {len(rooms)}")
    if not rooms:
        print("❌ No rooms available in that window. Change the time.")
        return

    chosen = rooms[0]
    room_id = chosen.get("id")
    print("✅ Chosen room:", chosen, "\n")

    # Book it
    booking = book_room(token, room_id, start_time, end_time, no_of_persons=1)
    print("BOOK RESULT:", booking, "\n")

# My bookings
    my = get_my_bookings(token)
    print("✅ MY BOOKINGS:", my)

# Cancel booking 
    if isinstance(my, list) and my:
        booking_id = my[0].get("id")
        cancel_result = cancel_booking(token, booking_id)
        print("✅ CANCEL RESULT:", cancel_result)
    else:
        print("⚠️ No bookings found to cancel.")

if __name__ == "__main__":
    main()
