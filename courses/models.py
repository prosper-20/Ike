from __future__ import unicode_literals
from pyexpat import model
from xml.sax.handler import property_interning_dict
from django.db import models
from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from django.utils import timezone

User= get_user_model()

class Course(models.Model):
    # user=  models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='posts')
    course= models.CharField(max_length=355)
    # course_link = models.CharField(max_length=700)
    date_added = models.DateTimeField(auto_now_add=True)

    
    
    def __str__(self) -> str:
        return self.course
        # f"{self.User} chose {}"


class Selection(models.Model):
    user = models.ForeignKey(User, null= True,blank= True, on_delete=models.CASCADE, related_name='selections')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="selections")
    date_added = models.DateTimeField(auto_now_add=True)  

    def __str__(self) -> str:
        return self.user

    @property
    def course_detail(self):
        return model_to_dict(self.course)

class UserCourses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="usercourses")
    chosen_courses= models.ForeignKey(Selection, on_delete=models.CASCADE, related_name='usercourses')

    def __str__(self) -> str:
        return f"{self.user} chose {self.chosen_courses}"

    @property
    def chosen_courses(self):
        return model_to_dict(self.chosen_courses)

class AccessCourse(models.Model):
    code = models.CharField(max_length=200)
    user= models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.code} >>> {self.user.email}'