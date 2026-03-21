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

def remove_room_flow():
    from apps.booking.utils import remove_room_and_get_affected_users
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

def add_room_flow():
    from apps.booking.utils import add_room

    room_name = input("Enter room name: ")
    capacity = input("Enter room capacity: ")

    try:
        capacity = int(capacity)
    except ValueError:
        print("Invalid capacity")
        return

    room = add_room(room_name, capacity)
    print(f"Room '{room.room_name}' added with ID {room.id}")


def change_capacity_flow():
    from apps.booking.utils import change_room_capacity

    room_id = input("Enter Room ID: ")
    new_capacity = input("Enter new capacity: ")

    try:
        room_id = int(room_id)
        new_capacity = int(new_capacity)
    except ValueError:
        print("Invalid input")
        return

    room = change_room_capacity(room_id, new_capacity)

    if room is None:
        print("Room not found")
        return

    print(f"Room '{room.room_name}' capacity updated to {new_capacity}")

def main():
    while True:
        print("\n===== MENU =====")
        print("\nRoom Management")
        print("1. Add Room")
        print("2. Remove Room")
        print("3. Change Capacity")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_room_flow()
        elif choice == "2":
            remove_room_flow()
        elif choice == "3":
            change_capacity_flow()
        elif choice == "4":
            print("Goodbye")
            break
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()