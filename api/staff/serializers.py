from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from staff.models import *


class BithdaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ["bithday"]


class StardetDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = ["stardet_day"]


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = "__all__"


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username"]


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]


class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = User
        fields = ["id","username", "token","is_superuser"]

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)


class StaffListSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer()
    profession = ProfessionSerializer()
    class Meta:
        model = Staff
        fields = ["fullname", "department", "profession"]


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        exclude = ["user"]