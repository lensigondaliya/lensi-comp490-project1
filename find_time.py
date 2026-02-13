import os
from datetime import datetime, timedelta

from skills import login_access_token, get_available_rooms

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

def fmt(dt: datetime) -> str:
    # same format your server expects (matches README example)
    return dt.strftime("%Y-%m-%d %I:%M %p")

def main():
    token = login_access_token(EMAIL, PASSWORD)

    base = datetime(2026, 2, 20, 8, 0)  # start scanning at 8:00 AM
    for i in range(0, 14 * 4):          # 14 hours, every 15 minutes
        start = base + timedelta(minutes=15 * i)
        end = start + timedelta(minutes=15)

        rooms = get_available_rooms(token, fmt(start), fmt(end))
        if rooms:
            print("\nFOUND ROOMS!")
            print("start:", fmt(start))
            print("end  :", fmt(end))
            print("count:", len(rooms))
            print("first room:", rooms[0])
            return

    print("No rooms found in the whole scan range.")

if __name__ == "__main__":
    main()
