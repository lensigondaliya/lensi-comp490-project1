# imports
from rest_framework import generics
from django.db.models import Q
from Room_booking_serve.apps.booking.models import MeetingRoom , BookingHistory
from rest_api.booking.utils import is_meeting_room_available, send_cancellation_email, send_confirmation_email
from .serializers import MeetingRoomSerializer
from .serializers import BookingHistorySerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import SessionAuthentication
import threading
from django.utils import timezone
from datetime import datetime
from rest_framework.views import APIView



class MeetingRoomListView(generics.ListCreateAPIView):
    authentication_classes = [SessionAuthentication]
    serializer_class = MeetingRoomSerializer
    permission_classes = [IsAuthenticated]
    queryset = MeetingRoom.objects.all()

    # def get_permissions(self):
    #     if self.request.method == "POST":
    #         permission_classes = [IsAdminUser]
    #     else:
    #         permission_classes = [IsAuthenticated]
    #     return [permission() for permission in permission_classes]
    
class MeetingRoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = []
    permission_classes = [IsAdminUser]
    queryset = MeetingRoom.objects.all()
    serializer_class = MeetingRoomSerializer
    lookup_url_kwarg = "room_id"

    def delete(self, request, *args, **kwargs):
        room = self.get_object()

        # 1. get all bookings for this room
        bookings = BookingHistory.objects.filter(meeting_room=room)

        # 2. collect usernames
        usernames = [b.booked_by.username for b in bookings]

        # 3. Save usernames to report
        if usernames:
            with open("cancellation_report.txt", "w", encoding="utf-8") as f:
                for username in usernames:
                    f.write(username + "\n")


        # 4. delete room 
        room.delete()

        return Response(status=204)

    

    def get_queryset(self):
        start_time = self.request.query_params.get('start_time', None)
        end_time = self.request.query_params.get('end_time', None)

        # Filter by time if provided
        if start_time and end_time:
            from django.utils.dateparse import parse_datetime
            if not parse_datetime(start_time) or not parse_datetime(end_time):
                return MeetingRoom.objects.none()

            # Return available rooms
            queryset = MeetingRoom.objects.filter(
                Q(booking_histories__end_time__lte=start_time) | Q(booking_histories__start_time__gte=end_time) | Q(booking_histories__isnull=True),
                is_active=True
            ).distinct()
        else:
            # Return all active rooms
            queryset = MeetingRoom.objects.filter(is_active=True)

        return queryset


class MeetingRoomBookingView(generics.CreateAPIView):
   # Book a meeting room
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BookingHistorySerializer
    queryset = MeetingRoom.objects.all()


    def create(self, request, *args, **kwargs):
        room_id = self.kwargs.get('room_id')
        start_time_str = request.data.get('start_time')
        end_time_str = request.data.get('end_time')
        no_of_persons = request.data.get('no_of_persons', 1)  
        
        # Convert input times
        start_time = datetime.strptime(start_time_str, '%Y-%m-%d %I:%M %p')
        end_time = datetime.strptime(end_time_str, '%Y-%m-%d %I:%M %p')
        
        try:
            meeting_room = MeetingRoom.objects.get(pk=room_id, is_active=True)
        except MeetingRoom.DoesNotExist:
            return Response({"error": "Meeting room not found."}, status=status.HTTP_404_NOT_FOUND)

        # Prepare serializer data
        serializer = self.get_serializer(data={
            "start_time": start_time.isoformat(),
            "end_time": end_time.isoformat(),
            "no_of_persons": no_of_persons,
        })
        serializer.is_valid(raise_exception=True)

        # Check room availability and capacity
        if not is_meeting_room_available(meeting_room, start_time, end_time) or meeting_room.capacity < no_of_persons:
            return Response({"error": "Meeting room is not available or does not have sufficient capacity for the specified time range and number of persons."}, status=status.HTTP_400_BAD_REQUEST)

        serializer.save(meeting_room=meeting_room, booked_by=request.user, no_of_persons=no_of_persons)

        # Send confirmation email in background
        thread = threading.Thread(
            target=send_confirmation_email,
            args=(
                meeting_room.room_name,
                serializer.instance.start_time,
                serializer.instance.end_time,
                request.user.email,
            )
        )
        thread.start()

        return Response({"message": "Meeting room booked successfully."}, status=status.HTTP_201_CREATED)



class MyBookingsView(APIView):
   # Show current user's bookings
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        bookings = BookingHistory.objects.filter(booked_by=user)
        serializer = BookingHistorySerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


class CancelMeetingRoomBookingView(generics.DestroyAPIView):
    # Cancel a meeting room booking
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = BookingHistorySerializer

    def destroy(self, request, *args, **kwargs):
        booking_id = self.kwargs.get('booking_id')
    

        try:
            booking = BookingHistory.objects.get(pk=booking_id, booked_by=request.user)
        except BookingHistory.DoesNotExist:
            return Response({"error": "Meeting room booking not found or you are not authorized to cancel this booking."}, status=status.HTTP_404_NOT_FOUND)

        # Do not allow cancellation after start time
        current_time = timezone.now()
        if booking.start_time <= current_time:
            return Response({"error": "Meeting room booking cannot be canceled as the start time has already passed."}, status=status.HTTP_400_BAD_REQUEST)

        booking.delete()

        # Create a thread to send the cancellation email with necessary data
        thread = threading.Thread(
            target=send_cancellation_email,
            args=(
                booking.meeting_room.room_name,
                booking.start_time,
                booking.end_time,
                request.user.email,
            )
        )
        thread.start()

        return Response({"message": "Your Meeting Room Booking has been cancelled!"}, status=status.HTTP_204_NO_CONTENT)
    