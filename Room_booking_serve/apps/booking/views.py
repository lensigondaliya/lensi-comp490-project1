from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import MeetingRoom, BookingHistory


@api_view(['POST'])
def add_room(request):
    room_name = request.data.get('room_name')
    capacity = request.data.get('capacity')

    if not room_name or not capacity:
        return Response({"error": "Missing data"}, status=400)

    room = MeetingRoom.objects.create(
        room_name=room_name,
        capacity=capacity
    )


    return Response({"message": f"Room '{room.room_name}' created"}, status=201)


@api_view(['PATCH'])
def update_room_capacity(request, room_id):
    new_capacity = request.data.get('capacity')

    if not new_capacity:
        return Response({"error": "Missing capacity"}, status=400)

    try:
        room = MeetingRoom.objects.get(id=room_id)
    except MeetingRoom.DoesNotExist:
        return Response({"error": "Room not found"}, status=404)

    room.capacity = new_capacity
    room.save()

    return Response(
        {"message": f"Room '{room.room_name}' capacity updated to {room.capacity}"},
        status=200
    )

@api_view(['DELETE'])
def remove_room(request, room_id):
    try:
        room = MeetingRoom.objects.get(id=room_id)
    except MeetingRoom.DoesNotExist:
        return Response({"error": "Room not found"}, status=404)

    cancelled_usernames = list(
        BookingHistory.objects.filter(meeting_room=room)
        .values_list('booked_by__username', flat=True)
        .distinct()
    )

    room.delete()

    return Response(
        {
            "message": f"Room '{room.room_name}' removed",
            "cancelled_usernames": cancelled_usernames
        },
        status=200
    )