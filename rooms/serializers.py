from rest_framework import serializers
from users.serializers import RelatedUserSerializer, UserSerializer
from .models import Room,Photo


# class ReadRoomSerializer(serializers.ModelSerializer):
#     user = RelatedUserSerializer()
#
#     class Meta:
#         model = Room
#         exclude = ("modified",)
#         # fields = ("pk", "name", "price", "user")
class PhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo
        exclude = ("room",)

class RoomSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    is_fav = serializers.SerializerMethodField()
    photos = PhotoSerializer(read_only=True, many=True)

    class Meta:
        model = Room
        exclude = ("modified",)
        read_only_fields = ["user", "id", "created", "updated"]

    def validate(self, data):
        if self.instance:  # instance가있으면 업데이트를 한다는 말
            check_in = data.get("check_in", self.instance.check_in)
            check_out = data.get("check_out", self.instance.check_out)  # 데이터가 없으면 self.instance.check_out를 넣는다
        else:
            check_in = data.get('check_in')
            check_out = data.get('check_out')
        if check_in == check_out:
            raise serializers.ValidationError('Not enough time between changes')
        return data

    def get_is_fav(self, obj):

        request = self.context.get("request")
        if request:
            user = request.user
            if user.is_authenticated:
                return obj in user.favs.all()
        return False

    def create(self, validated_data):
        request = self.context.get("request")
        room = Room.objects.create(**validated_data, user=request.user)
        return room

    #     아래 소스를 ModelSerializer를써서 간편하게
    # name = serializers.CharField(max_length=140)
    # address = serializers.CharField(max_length=140)
    # price = serializers.IntegerField()
    # beds = serializers.IntegerField(default=1)
    # lat = serializers.DecimalField(max_digits=10, decimal_places=6)
    # lng = serializers.DecimalField(max_digits=10, decimal_places=6)
    # bedrooms = serializers.IntegerField(default=1)
    # bathrooms = serializers.IntegerField(default=1)
    # check_in = serializers.TimeField(default="00:00:00")
    # check_out = serializers.TimeField(default="00:00:00")
    # instant_book = serializers.BooleanField(default=False)

    # def create(self, validated_data):
    #     return Room.objects.create(**validated_data)

    #
    #

    # def update(self, instance, validated_data):
    #     instance.name = validated_data.get("name", instance.name)
    #     instance.address = validated_data.get("address", instance.address)
    #     instance.price = validated_data.get("price", instance.price)
    #     instance.beds = validated_data.get("beds", instance.beds)
    #     instance.lat = validated_data.get("lat", instance.lat)
    #     instance.lng = validated_data.get("lng", instance.lng)
    #     instance.bedrooms = validated_data.get("bedrooms", instance.bedrooms)
    #     instance.bathrooms = validated_data.get("bathrooms", instance.bathrooms)
    #     instance.check_in = validated_data.get("check_in", instance.check_in)
    #     instance.check_out = validated_data.get("check_out", instance.check_out)
    #     instance.instant_book = validated_data.get("instant_book", instance.instant_book)
    #     instance.save()
    #     return instance
    #
    #
    #
    #
    # def validate_beds(self, beds):
    #     if beds < 5:
    #         raise serializers.ValidationError("Your house is too small")
    #     else:
    #         return beds
