import os
import sys
import django

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.join(BASE_DIR, "Room_booking_serve")

sys.path.insert(0, PROJECT_DIR)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "meeting_room_booking.settings"
)

django.setup()

from apps.booking.utils import remove_room_and_get_affected_users

def remove_room_flow():
    room_id = input("Enter Room ID to remove: ")
    try:
        room_id = int(room_id)
    except ValueError:
        print("Invalid room ID")
        return

    room_name, users = remove_room_and_get_affected_users(room_id)

    if room_name is None:
        print("Room not found")
        return

    print(f"\nRoom '{room_name}' deleted.")

    if users:
        print("Users whose reservations were canceled:")
    
    with open("cancellation_report.txt", "w") as f: 
        f.write(f"Room '{room_name}' deleted\n") 
        f.write("Affected users:\n")

    for user in users:
        print(f"- {user}")
        f.write(f"- {user}\n")
        

        print("\nReport saved to cancellation_report.txt")

    else:
        print("No reservations were affected.")


def main():
    print("\n===== MENU =====")
print("1. Remove Room")
choice = input("Enter choice: ")

if choice == "1":
    remove_room_flow()
else:
    print("Invalid choice")
if __name__ == "main":
    main()

# EMAIL = "test@gmail.com"
# PASSWORD = "123456"

# print("DEBUG EMAIL:", EMAIL)

# # Time format required by server
# def fmt(dt: datetime) -> str:
#     return dt.strftime("%Y-%m-%d %I:%M %p")


# def main():
#     def remove_room_flow():
#      room_id = input("Enter Room ID to remove: ")

#     try:
#         room_id = int(room_id)
#     except ValueError:
#         print("Invalid room ID")
#         return

#     room_name, users = remove_room_and_get_affected_users(room_id)

#     if room_name is None:
#         print("Room not found")
#         return

#     print(f"\nRoom '{room_name}' deleted.")

#     if users:
#         print("Users whose reservations were canceled:")
#         for user in users:
#             print(f"- {user}")
#     else:
#         print("No reservations were affected.")


# def main():
#     print("\n===== MENU =====")
#     print("1. Remove Room")

#     choice = input("Enter choice: ")

#     if choice == "1":
#         remove_room_flow()
#     else:
#         print("Invalid choice")

