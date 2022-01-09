from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views

# app_name = "rooms"

# router = DefaultRouter()
# router.register("", viewsets.RoomViewset, basename="room")
# urlpatterns = router.urls

urlpatterns = [
    path("", views.ListRoomsView.as_view()),
    path("<int:pk>/", views.SeeRoomView.as_view()),
]
