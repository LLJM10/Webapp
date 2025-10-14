from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    profile = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "profile"]

    def get_profile(self, obj):
        try:
            profile = UserProfile.objects.get(user=obj)
            return {
                "role": profile.role,
                "bio": profile.bio,
                "created_at": profile.created_at
            }
        except UserProfile.DoesNotExist:
            return None

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    role = serializers.CharField(required=True)

    class Meta:
        model = UserProfile
        fields = ["id", "user", "role", "bio", "created_at"]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        role = validated_data.pop('role', 'startup')
        user = User.objects.create_user(**user_data)
        profile = UserProfile.objects.create(user=user, role=role, **validated_data)
        return profile
