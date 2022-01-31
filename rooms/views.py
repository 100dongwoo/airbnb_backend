from django.http import response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Room
from .serializers import RoomSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework import permissions
from .permissions import IsOwner
from rest_framework.decorators import action


# class ListRoomsView(ListAPIView):
#     # ListAPIView
#     queryset = Room.objects.all()
#     serializer_class = RoomSerializer

#  이 아래
# @api_view(["GET", "POST"])
# def rooms_view(request):
#     if request.method == "GET":
#         rooms = Room.objects.all()[:5]
#         serializer = RoomSerializer(rooms, many=True).data
#         return Response(serializer)
#
#     elif request.method == "POST":
#         if not request.user.is_authenticated:
#             return Response(status=status.HTTP_401_UNAUTHORIZED)
#         serializer = RoomSerializer(data=request.data)
#
#         if serializer.is_valid():
#             room = serializer.save(user=request.user)
#             room_serializer = RoomSerializer(room).data
#             return Response(data=room_serializer, status=status.HTTP_200_OK)
#         else:
#             return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class OwnPagination(PageNumberPagination):
#     page_size = 20


# class RoomsView(APIView):
#     def get(self, request):
#         paginator = OwnPagination()
#         rooms = Room.objects.all()
#         results = paginator.paginate_queryset(rooms, request)
#         serializer = RoomSerializer(results, many=True, context={"request": request})
#         return paginator.get_paginated_response(serializer.data)
#
#     def post(self, request):
#         if not request.user.is_authenticated:
#             return Response(status=status.HTTP_401_UNAUTHORIZED)
#         serializer = RoomSerializer(data=request.data)
#
#         if serializer.is_valid():
#             room = serializer.save(user=request.user)
#             room_serializer = RoomSerializer(room).data
#             return Response(data=room_serializer, status=status.HTTP_200_OK)
#         else:
#             return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class RoomView(APIView):
#     def get_room(self, pk):
#         try:
#             room = Room.objects.get(pk=pk)
#             return room
#         except Room.DoesNotExist:
#             return None
#
#     def get(self, request, pk):
#         room = self.get_room(pk)
#         if room is not None:
#             serializer = RoomSerializer(room, context={"request": request}).data
#             return Response(serializer)
#         else:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#     def put(self, request, pk):
#         room = self.get_room(pk)
#         if room is not None:
#             if room.user != request.user:
#                 return Response(status=status.HTTP_403_FORBIDDEN)
#             serializer = RoomSerializer(room, data=request.data, partial=True)
#             if serializer.is_valid():
#                 room = serializer.save()  # update
#                 return Response(RoomSerializer(room).data)  # 바로 결과 값 보여주는거
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#             return Response()
#         else:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#
#     def delete(self, request, pk):
#         room = self.get_room(pk)
#         if room.user != request.user:
#             return Response(status=status.HTTP_403_FORBIDDEN)
#         if room is not None:
#             room.delete()
#             return Response(status=status.HTTP_200_OK)
#         else:
#             return Response(status=status.HTTP_404_NOT_FOUND)


#  viewset
class RoomViewSet(ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_permissions(self):
        if self.action == "list" or self.action == "retrieve":
            permission_classes = [permissions.AllowAny]
        elif self.action == "create":
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]

    # ->위에 return과 아래 3줄이 같은의미
    # for p in permission_classes:
    #       called_perm,.apeend(p(())
    #      return [permission() for permission in permission_classes

    @action(detail=False)
    # 아래 이름이 url이름이다
    def search(self, request):
        max_price = request.GET.get("max_price", None)
        min_price = request.GET.get("min_price", None)
        beds = request.GET.get("beds", None)
        bedrooms = request.GET.get("bedrooms", None)
        bathrooms = request.GET.get("bathrooms", None)
        lat = request.GET.get("lat", None)
        lng = request.GET.get("lng", None)
        filter_kwargs = {}
        if max_price is not None:
            filter_kwargs["price__lte"] = max_price
        if min_price is not None:
            filter_kwargs["price__gte"] = min_price
        if beds is not None:
            filter_kwargs["beds__gte"] = beds
        if bedrooms is not None:
            filter_kwargs["bedrooms__gte"] = bedrooms
        if bathrooms is not None:
            filter_kwargs["bathrooms__gte"] = bathrooms
        paginator = self.paginator
        # modelviewset에는 paginator 존재

        if lat is not None and lng is not None:
            filter_kwargs["lat__gte"] = float(lat) - 0.005
            filter_kwargs["lat__lte"] = float(lat) + 0.005
            filter_kwargs["lng__gte"] = float(lng) - 0.005
            filter_kwargs["lng__lte"] = float(lng) + 0.005

        try:
            rooms = Room.objects.filter(**filter_kwargs)
        except:
            rooms = Room.objects.all()
        results = paginator.paginate_queryset(rooms, request)
        serializer = RoomSerializer(results, many=True,context={"request": request})
        return paginator.get_paginated_response(serializer.data)

#
#
# @api_view(["GET"])
# def room_search(request):
#     max_price = request.GET.get("max_price", None)
#     min_price = request.GET.get("min_price", None)
#     beds = request.GET.get("beds", None)
#     bedrooms = request.GET.get("bedrooms", None)
#     bathrooms = request.GET.get("bathrooms", None)
#     lat = request.GET.get("lat", None)
#     lng = request.GET.get("lng", None)
#     filter_kwargs = {}
#     if max_price is not None:
#         filter_kwargs["price__lte"] = max_price
#     if min_price is not None:
#         filter_kwargs["price__gte"] = min_price
#     if beds is not None:
#         filter_kwargs["beds__gte"] = beds
#     if bedrooms is not None:
#         filter_kwargs["bedrooms__gte"] = bedrooms
#     if bathrooms is not None:
#         filter_kwargs["bathrooms__gte"] = bathrooms
#     # paginator = OwnPagination()
#
#     if lat is not None and lng is not None:
#         filter_kwargs["lat__gte"] = float(lat) - 0.005
#         filter_kwargs["lat__lte"] = float(lat) + 0.005
#         filter_kwargs["lng__gte"] = float(lng) - 0.005
#         filter_kwargs["lng__lte"] = float(lng) + 0.005
#
#     try:
#         rooms = Room.objects.filter(**filter_kwargs)
#     except:
#         print(filter_kwargs)
#         rooms = Room.objects.all()
#     results = paginator.paginate_queryset(rooms, request)
#     serializers = RoomSerializer(results, many=True, )
#     return paginator.get_paginated_response(serializers.data)

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
