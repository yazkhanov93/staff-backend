from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import permission_classes
from rest_framework import status
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import Q
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .serializers import *
from staff.models import *


class StatisticView(APIView):
    def get(self, request):
        try:
            staff=Staff.objects.all()
            department = staff.filter(department__dep_name__icontains="kafedrasy").count()
            gdech = staff.filter(department__dep_name__icontains="ylmy merkezi").count()
            hb = staff.filter(department__dep_name__icontains="Hojalyk bölümi").count()
            h = staff.filter(department__dep_name__icontains="Hünärmenler").count()
            professor = staff.filter(profession__title__icontains="Professor").count()
            seniorTeacher = staff.filter(profession__title__icontains="Uly mugallym").count()
            teacher = staff.filter(profession__title__icontains="Mugallym").count()
            interns = staff.filter(profession__title__icontains="Öwrenje mugallym").count()
            allTeachers = professor + seniorTeacher + teacher + interns
            return Response({"Kafedralar":department,"'GDEÇ' ylmy merkezi":gdech, "Hojalyk bölümi":hb, "Hünärmenler":h, "Ähli işgärler":staff.count(), "Professorlar":professor, "Uly mugallymlar":seniorTeacher, "Mugallym":teacher,"Öwrenje mugallymlar":interns, "Ähli mugallymlar":allTeachers})
        except Exception as e:
            raise  ParseError(e)


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
    search = openapi.Parameter("search", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
                               description="Global Search")
    started_day = openapi.Parameter("started_day", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
                               description="Format yy-mm-dd")
    birthday = openapi.Parameter("birthday", in_=openapi.IN_QUERY, type=openapi.TYPE_STRING,
                               description="Format yy-mm-dd")
    profession = openapi.Parameter("profession", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                               description="Profession")
    department = openapi.Parameter("department", in_=openapi.IN_QUERY, type=openapi.TYPE_INTEGER,
                               description="department")
    @swagger_auto_schema(manual_parameters=[search,started_day,birthday,profession,department])
    def get(self, request):
        try:
            staff = Staff.objects.all()
            if request.query_params.get("search", None):
                search = request.query_params.get("search", None)
                staff = staff.filter(Q(fullname=search)|Q(working_for__icontains=search)|Q(languages__icontains=search)|Q(another_country__icontains=search)|Q(deputy=search)|Q(party_member=search)|Q(prev_place=search))
            if request.query_params.get("started_day", None):
                started_day = request.query_params.get("started_day", None)
                staff = staff.filter(stardet_day=stardet_day)
            if request.query_params.get("birthday", None):
                birthday = request.query_params.get("birthday", None)
                staff = staff.filter(birthday=birthday)
            if request.query_params.get("profession", None):
                profession = request.query_params.get("profession", None)
                staff = staff.filter(profession=profession)
            if request.query_params.get("department", None):
                department = request.query_params.get("department", None)
                staff = staff.filter(department=department)
            serializer = StaffListSerializer(staff, many=True)
            return Response(serializer.data)
        except Exception as e:
            raise ParseError(e)


class BirthdayView(APIView):

    def get(self, request):
        try:
            birthday = Staff.objects.all().only("birthday")
            serializer = BirthdaySerializer(birthday, many=True)
            return Response(serializer.data)
        except Exception as e:
            raise ParseError(e)


class StartedDayView(APIView):

    def get(self, request):
        try:
            started_day = Staff.objects.all().only("started_day")
            serializer = StartedDaySerializer(started_day, many=True)
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