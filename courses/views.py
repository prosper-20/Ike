from django.forms import model_to_dict
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .models import Course,Selection
from .serializers import CourseSerializer,SelectionSerializer,NewSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, PermissionDenied
from django.contrib.auth import get_user_model




User= get_user_model()

@swagger_auto_schema(methods=['POST'] ,
                    request_body=CourseSerializer())
@api_view(['POST', 'GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def create_courses(request):
    user= request.user
    # print(user)
    if request.method == 'POST':
        if request.user.is_superuser != True:
            raise PermissionDenied(detail={'message':'You do not have permission to add courses!'})
        
        serializer = CourseSerializer(data=request.data)
        
        if serializer.is_valid():
            if user in User.objects.filter(is_superuser= True):
                course= serializer.validated_data['course']

                course_= Course.objects.create(course=course)
                new_serializer= CourseSerializer(course_)

                data = {
                "message":"successful",
                "data": new_serializer.data
                }
                return Response(data, status=status.HTTP_200_OK)
            
            else:
                data = {
                    'message' : 'Log into an admin account to perform this action',
                    'error'  : serializer.errors
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST) 
        else:
            data = {
                'message' : 'failed',
                'error'  : serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "GET":
        courses_ = Course.objects.all()
        serializer = CourseSerializer(courses_, many=True)
        
        data = {
           "message":"All Courses Below",
           "data": serializer.data
        }
    
    
        return Response(data, status=status.HTTP_200_OK)

@swagger_auto_schema(methods=['PUT'],
                    request_body=CourseSerializer())
@api_view(['GET','PUT','DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def course_detail(request, course_id):
    
    try:
        course__= Course.objects.get(id=course_id)
    except Course.DoesNotExist:
        data= {
            'message': 'failed',
            'error': f"Post with ID {course_id} does not exist."
        }
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer= CourseSerializer(course__)

        data = {
                'message' : 'successful',
                'data'  : serializer.data
            }
        return Response(data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        # if course__.user != request.user:
        if request.user.is_superuser != True:
                raise PermissionDenied(detail={'message':'You do not have permission to edit!'})    
        serializer = CourseSerializer(course__, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            data = {
                'message' : 'successful',
                'data'  : serializer.data
            }
            return Response(data, status=status.HTTP_202_ACCEPTED)

        else:
            data = {
                'message' : 'failed',
                'error'  : serializer.errors
            }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if request.user.is_superuser != True:
            # if course__.user != request.user:
                raise PermissionDenied(detail={'message':'You do not have permission to delete!'})
        elif request.user.is_superuser == True:
           course__.delete()
           data = {
                'message' : 'Course deleted successfully!',
            }
        return Response(data, status=status.HTTP_204_NO_CONTENT)


@swagger_auto_schema(methods=['POST'] ,
                    request_body=SelectionSerializer())
@api_view(['GET', 'POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def selected_courses(request):
    user= request.user
    if request.method == "GET":
        selected = Selection.objects.filter(user=user)
        serializer = SelectionSerializer(selected, many=True)
        
        data = {
           "message":"successful",
           "data": serializer.data
        }
    
    
        return Response(data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        if user == request.user:
            serializer = SelectionSerializer(data=request.data)
            if serializer.is_valid(): 
                if "user" in serializer.validated_data.keys():
                    serializer.validated_data.pop("user")
                # print(serializer.validated_data)  
                course = serializer.validated_data["course"]
                
                # print(song)
                selected_ = Selection.objects.create(user=user,course=course)
                new_serializer = SelectionSerializer(selected_)
                
                data = {
                    'message' : 'success',
                    'data'  : new_serializer.data
                }
                return Response(data, status=status.HTTP_202_ACCEPTED)
            else:
                data = {
                    'message' : 'failed',
                    'error'  : serializer.errors
                }
                return Response(data, status=status.HTTP_400_BAD_REQUEST)
        
    
    
    

    
    

@api_view(['GET', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def selection_detail(request, selection_id):

    
    try:
        selected__ = Selection.objects.get(id=selection_id)
    except Selection.DoesNotExist:

        data = {
            'message' : 'failed',
            'error'  : f"Playlist with ID {selection_id} does not exist."
        }
        return Response(data, status=status.HTTP_404_NOT_FOUND)
    if selected__.user != request.user:
        raise PermissionDenied(detail={"message":"You do not have the permission to view this item."})
    
    if request.method == "GET":
        serializer = SelectionSerializer(selected__)
        
        data = {
           "message":"successful",
           "data": serializer.data
        }
    
    
        return Response(data, status=status.HTTP_200_OK)
    
    elif request.method=="DELETE":
        selected__.delete()
        
        return Response({}, status=status.HTTP_204_NO_CONTENT)

@swagger_auto_schema(methods=['put'] ,
                    request_body=NewSerializer())
@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def payment(request):
    user = request.user

    if request.method == 'PUT':
        if request.user.is_payment == True:
            raise PermissionDenied(detail={'message':'Payment has been made already'})

        serializer = NewSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            if request.user.is_payment != True:
                request.user.is_payment == True
            # if 'password' in serializer.validated_data.keys():
            #     raise ValidationError(detail={
            #         "message":"Edit password action not allowed"
            #     }, code=status.HTTP_403_FORBIDDEN)
                
            serializer.save()
            data = {
                'message' : 'success',
                'data'  : serializer.data
            }
            return Response(data, status=status.HTTP_202_ACCEPTED)
        else:
            data = {
                'message' : 'failed',
                'error'  : serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)



# @api_view(['GET'])
# @authentication_classes([BasicAuthentication])
# def get_selections(request):
#     if request.method == 'GET':
#         #Get all the users in the database
#         all_selections= Selection.objects.all()
        

#         serializer = SelectionSerializer(all_selections,many=True)

#         serializer_list = []
#         for i in serializer.data:
#             user_id = i['user']
#             user= User.objects.get(id= user_id)
#             user_dict=model_to_dict(user, ['id',
#                                     'first_name'
#                                     ,'last_name'])
#             user_dict['selection_id'] = i['id']
#             user_dict['message'] = i['message']
#             user_dict['date_added'] = i['date_added']
#             serializer_list.append(user_dict)
#         data = {
#                 'message' : 'successful',
#                 'data'  : serializer_list
#             }
#         return Response(data, status=status.HTTP_200_OK)    