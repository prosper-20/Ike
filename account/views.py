from rest_framework.response import Response
from rest_framework import status 
from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import ResendOTPSerializer, UserSerializer, LoginSerializer, VerifyOTPSerializer, ResetSerializer,ForgotSerializer,VerifyPasswordOTPSerializer
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth import authenticate
from django.forms import model_to_dict
from rest_framework.exceptions import ValidationError,PermissionDenied
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token

User = get_user_model()


@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def user_view(request):
    
    if request.method == 'GET':
        # Get all the users in the database
        all_users = User.objects.all()
        
        serializer = UserSerializer(all_users, many=True)
        
        data = {
           "message":"successful",
           "data": serializer.data
        }
    
    
        # return JsonResponse(data)
        return Response(data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='post', 
                    request_body=UserSerializer(),
                    operation_description="This is a function to create new users.",
                    responses= {201: openapi.Response("""An example success response is:
                    ``{
                        "message": "successful",
                        "data": [
                            {
                                "id": 1,
                                "first_name": "Test",
                                "last_name": "User",
                                "email": "test@user.com",
                                "phone": "234123456789",
                                "date_joined":"2022-01-26T10:33:45.239782Z"
                            }
                        ]
                    }``"""),
                        400: openapi.Response("""An example failure is:
                        ``{
                        "message": "failed",
                        "error": {
                            "email": [
                            "This field is required."
                            ],
                            "password": [
                            "This field is required."
                            ],
                            "phone": [
                            "This field is required."
                            ]
                        }``""")
                    }
)
@api_view(['POST'])
def create_account(request):
    
    if request.method == "POST":
        #Allows user to signup or create account
        serializer = UserSerializer(data=request.data) #deserialize the data
        
        if serializer.is_valid(): #validate the data that was passed
            serializer.save()
            data = {
                'message' : 'success',
                'data'  : serializer.data
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = {
                'message' : 'failed',
                'error'  : serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        

@swagger_auto_schema(method='post', 
                    request_body=LoginSerializer())
@api_view(['POST'])
def login_view(request):
    
    serializer = LoginSerializer(data=request.data)
    
    if serializer.is_valid():
        
        user = authenticate(email=serializer.validated_data['email'], password=serializer.validated_data['password'])
        
        if user: 
        
            data = {
                    'message' : 'success',
                    'data'  : model_to_dict(user, ['id', 
                                                   'first_name',
                                                   'last_name',
                                                   'email',
                                                   'phone',
                                                   'is_admin'])
                }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = {
                    'message' : 'Please enter a valid email and password'
                }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
    else:
        data = {
            'message' : 'failed',
            'error'  : serializer.errors
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)
    


@swagger_auto_schema(methods=['put'] ,
                    request_body=UserSerializer())
@api_view(['GET', 'PUT', 'DELETE'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def profile_view(request):
    user = request.user
    # user = User.objects.first()
    
    # try:
    #     user = User.objects.get(id=user_id)
    # except User.DoesNotExist:

    #     data = {
    #         'message' : 'failed',
    #         'error'  : f"User with ID {user_id} does not exist."
    #     }
    #     return Response(data, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = UserSerializer(user)
        
        data = {
           "message":"successful",
           "data": serializer.data
        }
    
    
        return Response(data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(): 
            if 'password' in serializer.validated_data.keys():
                raise ValidationError(detail={
                    "message":"Edit password action not allowed"
                }, code=status.HTTP_403_FORBIDDEN)
                
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
        
    elif request.method=="DELETE":
        user.delete()
        
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    

@swagger_auto_schema(methods=['POST'] ,
                    request_body=VerifyOTPSerializer())
@api_view(["POST"])
def verify_otp(request):
    serializer = VerifyOTPSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.verify()
        user_serializer = UserSerializer(user)
        data = {
            'message' : 'account activated',
            'data' : user_serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)
    
    
    
@swagger_auto_schema(methods=['POST'] ,
                    request_body=ResendOTPSerializer())
@api_view(["POST"])
def new_otp(request):
    serializer = ResendOTPSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.get_new_otp()
        
        return Response(data, status=status.HTTP_200_OK)

# Create your views here.
@swagger_auto_schema(methods=['put'] ,
                     request_body=ResetSerializer())
@api_view(['PUT'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def reset_password(request):
    user = request.user
    if request.method == 'PUT':
        serializer = ResetSerializer(data=request.data)
        if serializer.is_valid():  
            check = authenticate(email = user.email ,password=serializer.validated_data['old_password'])

            if check:
                if serializer.validated_data['password'] == serializer.validated_data['re_password']:

                    user.set_password(serializer.validated_data['password']) 
                    user.save()
                    data = {
                        'message' : 'success',
                        'data'  : serializer.data
                    }
                    return Response(data, status=status.HTTP_202_ACCEPTED)
                else:
                    data = {
                            'message' : "Passwords didn't match"
                        }
                    return Response(data, status=status.HTTP_401_UNAUTHORIZED)        
            else:
                data = {
                        'message' : 'Incorrect password'
                    }
                return Response(data, status=status.HTTP_401_UNAUTHORIZED)    
        else:
            data = {
                'message' : 'failed',
                'error'  : serializer.errors
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(methods=['post'] ,
                     request_body=ForgotSerializer())
@api_view(['POST'])
def forgot_password(request):

    serializer = ForgotSerializer(data=request.data)

    if serializer.is_valid():  
        mail = serializer.validated_data['email_forgot']
        check = User.objects.filter(email=mail)

        if check.exists():
            
            serializer.save()    
            data = {
                'message' : 'Success check your email',
                'data'  : serializer.data
            }    
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                'message' : f'Account with email: {mail} does not exist',
                
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)               
    else:
            data = {
                'message' : 'Serializer not valid',
                
            }
            return Response(data, status=status.HTTP_400_BAD_REQUEST)    
@swagger_auto_schema(methods=['POST'] ,
                    request_body=VerifyPasswordOTPSerializer())
@api_view(["POST"])
def verify_otp_pass(request):
    serializer = VerifyPasswordOTPSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.verify()
        if serializer.validated_data['password'] == serializer.validated_data['re_password']:
            user.set_password(serializer.validated_data['password']) 
            user.save()
            data = {
                'message' : 'success',
                'data'  : serializer.data
            }
            return Response(data, status=status.HTTP_202_ACCEPTED)
        else:
            data = {
                    'message' : "Passwords didn't match"
                }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)