from .models import MeetingRoom, BookingHistory


def remove_room_and_get_affected_users(room_id):
    try:
        room = MeetingRoom.objects.get(id=room_id)
    except MeetingRoom.DoesNotExist:
        return None, []

    # Get all bookings BEFORE deleting
    bookings = BookingHistory.objects.filter(meeting_room=room)

    affected_users = []
    for booking in bookings:
        affected_users.append(booking.booked_by.username)

    # Remove duplicates
    affected_users = list(set(affected_users))

    # Delete room (this deletes bookings automatically)
    room.delete()

    return room.room_name, affected_users

def add_room(room_name, capacity):
    room = MeetingRoom.objects.create(room_name=room_name, capacity=capacity)
    return room


def change_room_capacity(room_id, new_capacity):
    try:
        room = MeetingRoom.objects.get(id=room_id)
    except MeetingRoom.DoesNotExist:
        return None

    room.capacity = new_capacity
    room.save()
    return room
