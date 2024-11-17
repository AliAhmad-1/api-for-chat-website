from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from .serializers import *
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveUpdateAPIView




def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class RegisterView(APIView):
    def post(self,request,format=None):
        serializer=RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'msg':'your account created successfully'},status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self,request,format=None):
        serializer=LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username=serializer.data.get('username')
        password=serializer.data.get('password')
       
        user=authenticate(username=username,password=password)
        if user is not None:
            token=get_tokens_for_user(user)
            return Response({'msg':'Login Success','access_token':token['access'],'refresh_token':token['refresh']},status=status.HTTP_200_OK)
        else:
            return Response({'error':{'non_field_errors':['Email or Password not Valid ']}},status=status.HTTP_404_NOT_FOUND)
            

class LogoutUserView(APIView):
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]
    def post(self,request,format=None):
        serializers=LogoutSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        return Response({'msg':'User logout succussfully'},status=status.HTTP_204_NO_CONTENT)


class ProfileView(RetrieveUpdateAPIView):
    serializer_class=ProfileSerializer
    authentication_classes=[JWTAuthentication]
    permission_classes=[IsAuthenticated]

    def get_object(self):
        return self.request.user
