from django.db import models
from  django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Department(models.Model):
    dep_name = models.CharField(max_length=255, verbose_name="Department name")

    class Meta:
        verbose_name_plural = "Departments"

    def __str__(self):
        return self.dep_name


class Profession(models.Model):
    title = models.CharField(max_length=255, verbose_name="Profession title")

    class Meta:
        verbose_name_plural = "Professions"

    def __str__(self):
        return self.title


class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="User", related_name="user")
    fullname = models.CharField(max_length=255, verbose_name="Full Name", blank=True, null=True)
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE, verbose_name="Profession", related_name="profession", blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE,verbose_name="Department", related_name="department", blank=True, null=True)
    birthday = models.DateField(auto_now_add=False, verbose_name="Bithday", blank=True, null=True)
    started_day = models.DateField(auto_now_add=False, verbose_name="Started Day", blank=True, null=True)
    working_for = models.CharField(max_length=255, verbose_name="Working For", blank=True, null=True)
    languages = models.CharField(max_length=255, verbose_name="Languages", blank=True, null=True)
    another_country = models.CharField(max_length=255, verbose_name="Another Country", blank=True, null=True)
    deputy = models.CharField(max_length=255, verbose_name="Deputy", blank=True, null=True)
    party_member = models.CharField(max_length=255, verbose_name="Party Member", blank=True, null=True)
    phone_number = models.CharField(max_length=255, verbose_name="Phone Number", blank=True, null=True)
    profile_photo = models.ImageField(upload_to="", verbose_name="Profile Photo", blank=True, null=True)
    prev_place = models.CharField(max_length=255, verbose_name="Prev Place", blank=True, null=True)

    class Meta:
        verbose_name_plural = "Staff"

    def __str__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_info(sender, instance, created, **kwargs):
        if created:
            staff = Staff(user=instance)
            staff.save()