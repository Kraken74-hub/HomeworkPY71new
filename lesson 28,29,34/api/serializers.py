from rest_framework import serializers
from .models import CustomUser, Event

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'notify')

    def create(self, validated_data):
        return CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )

class EventSerializer(serializers.ModelSerializer):
    # Выводим массив имен пользователей
    users = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Event
        fields = ('id', 'name', 'meeting_time', 'description', 'place', 'users')