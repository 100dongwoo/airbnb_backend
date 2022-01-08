from django.shortcuts import render
from rooms.models import Room


def list_rooms(request):
    rooms = Room.objects.all()
    print("list")
    print(rooms)


# Create your views here.
