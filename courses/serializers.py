from rest_framework import serializers
from .models import Course,Selection
from django.contrib.auth import get_user_model

User= get_user_model()

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model= Course
        fields= ['id','course']

class SelectionSerializer(serializers.ModelSerializer):
    course_detail = serializers.ReadOnlyField()

    class Meta:
        model= Selection
        fields= '__all__'


class UserChoseSerializer(serializers.ModelSerializer):
    chosen_courses = serializers.ReadOnlyField()

    class Meta:
        model= Selection
        fields= ['course','chosen_courses']

class NewSerializer(serializers.ModelSerializer):
    # password = serializers.CharField(max_length = 255, write_only=True)
    
    class Meta:
        model = User
        # fields = '__all__'
        fields = ['is_payment']