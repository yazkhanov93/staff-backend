from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema

from .serializers import *
from staff.models import *


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            staff = Staff.objects.get(user=request.user)
            serializer = StaffSerializer(staff, many=False)
            return Response(serializer.data)
        except Exception as e:
            raise ParseError(e)

    @swagger_auto_schema(request_body=StaffSerializer, response=StaffSerializer)
    def put(self, request):
        try:
            data = request.data
            staff = Staff.objects.get(user=request.user)
            serializer = StaffSerializer(staff, data=data)
            if  serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        except Exception as e:
            raise ParseError(e)


class StaffDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        try:
            staff = Staff.objects.get(id=pk)
            serializer = StaffSerializer(staff, many=False)
            return Response(serializer.data)
        except Exception as e:
            raise ParseError(e)


class StaffListView(APIView):

    def get(self, request):
        try:
            staff = Staff.objects.all()
            serializer = StaffListSerializer(staff, many=True)
            return Response(serializer.data)
        except Exception as e:
            raise ParseError(e)


class DepartmentView(APIView):
    @swagger_auto_schema(response=DepartmentSerializer)
    def get(self, request):
        try:
            department = Department.objects.all()
            serializer = DepartmentSerializer(department, many=True)
            return Response(serializer.data)
        except Exception as e:
            raise ParseError(e)


class ProfessionView(APIView):
    @swagger_auto_schema(response=ProfessionSerializer)
    def get(self, request):
        try:
            profession = Profession.objects.all()
            serializer = ProfessionSerializer(profession, many=True)
            return Response(serializer.data)
        except Exception as e:
            raise ParseError(e)


class RegisterUserView(APIView):
    @swagger_auto_schema(request_body=UserRegisterSerializer, response=UserRegisterSerializer)
    def post(self, request):
        try:
            data = request.data
            user = User.objects.create(
                username=data["username"],
                password=make_password(data["password"])
            )
            serializer = UserSerializerWithToken(user, many=False)
            return Response(serializer.data)
        except Exception as e:
            raise ParseError(e) 