# Generated by Django 4.2.1 on 2023-12-15 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0002_alter_staff_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='birthday',
            field=models.DateField(blank=True, null=True, verbose_name='Bithday'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='stardet_day',
            field=models.DateField(blank=True, null=True, verbose_name='Started Day'),
        ),
    ]