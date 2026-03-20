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
