# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class MainAppClassesinfo(models.Model):
    class_number = models.CharField(max_length=1024, blank=True, null=True)
    class_days = models.CharField(max_length=1024, blank=True, null=True)
    start_time = models.CharField(max_length=1024, blank=True, null=True)
    end_time = models.CharField(max_length=1024, blank=True, null=True)
    class_comments = models.CharField(max_length=1024, blank=True, null=True)
    instructor = models.CharField(max_length=1024, blank=True, null=True)
    room_num = models.ForeignKey('MainAppClassrooms', models.DO_NOTHING, db_column='room_num', blank=True, null=True)
    class_type = models.CharField(max_length=1024, blank=True, null=True)
    course_title = models.CharField(max_length=1024, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'main_app_classesinfo'


class MainAppClassrooms(models.Model):
    building = models.CharField(max_length=255)
    room_num = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'main_app_classrooms'
        unique_together = (('room_num', 'building'),)
