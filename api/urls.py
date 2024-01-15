from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from api.staff.views import *


urlpatterns = [
    path("birthday/", BirthdayView.as_view(), name="birthday"),
    path("started-day/", StartedDayView.as_view(), name="started-day"),
    path("user-profile/", UserProfileView.as_view(), name="user-profile"),
    path("staff-detail/<int:pk>/", StaffDetailView.as_view(), name="staff-detail"),
    path("staff-list/", StaffListView.as_view(), name="staff-list"),
    path("profession-list/", ProfessionView.as_view(), name="profession-list"),
    path("department-list/", DepartmentView.as_view(), name="department-list"),
    path("register/", RegisterUserView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login")
]