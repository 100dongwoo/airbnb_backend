# from rest_framework.views import APIView
from django.db.models import query
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from .models import Room
from .serializers import RoomSerializer


class ListRoomsView(ListAPIView):
    # ListAPIView
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class SeeRoomView(RetrieveAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

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
