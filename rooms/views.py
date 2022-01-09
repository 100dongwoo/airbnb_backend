from django.http import response
from rest_framework.generics import RetrieveAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Room
from .serializers import ReadRoomSerializer, WriteRoomSerializer
from rest_framework import status


# class ListRoomsView(ListAPIView):
#     # ListAPIView
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer


@api_view(["GET", "POST"])
def rooms_view(request):
    if request.method == "GET":
        rooms = Room.objects.all()[:5]
        serializer = ReadRoomSerializer(rooms, many=True).data
        return Response(serializer)

    elif request.method == "POST":
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = WriteRoomSerializer(data=request.data)

        if serializer.is_valid():
            room=serializer.save(user=request.user)
            room_serializer=ReadRoomSerializer(room).data
            return Response(data=room_serializer,status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)




class SeeRoomView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = ReadRoomSerializer

    # lookup_url_kwarg = "pkkk"

    #
    # # APIView
    # def get(self, request):
    #     rooms = Room.objects.all()
    #     serializer = RoomSerializer(rooms, many=True)
    #     return Response(serializer.data)

    # def post(self, request):
    #     pass


# @api_view(["GET"])
# def list_rooms(request):
#     rooms = Room.objects.all()
#     serialized_rooms = RoomSerializer(rooms, many=True)
#     return Response(data=serialized_rooms.data)


# Create your views here.
