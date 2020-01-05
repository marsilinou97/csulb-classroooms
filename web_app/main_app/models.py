from django.db import models


class Classrooms(models.Model):
    id = models.AutoField(primary_key=True)
    building = models.CharField(max_length=255)
    room_num = models.CharField(max_length=10)

class ClassesSessions(models.Model):
    id = models.AutoField(primary_key=True)
    room_id = models.ForeignKey(Classrooms, on_delete=models.CASCADE, default='-1')
    class_number = models.CharField(max_length=10)
    class_days = models.CharField(max_length=255)
    start_time = models.CharField(max_length=255)
    end_time = models.CharField(max_length=255)
    class_comments = models.CharField(max_length=1250)
    instructor = models.CharField(max_length=255)
    class_type = models.CharField(max_length=10)
    course_title = models.CharField(max_length=255)