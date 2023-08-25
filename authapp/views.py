from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from authapp.models import User
from authapp.serializers import UserCreationSerializer
from drf_yasg.utils import swagger_auto_schema

# Create your views here.
class HelloAuthView(generics.GenericAPIView):
    @swagger_auto_schema(operation_summary="Hello Auth")
    def get(self, request):
        return Response(data={'msg':"Hello Auth"}, status=status.HTTP_200_OK)



class UserCreationView(generics.GenericAPIView):
    serializer_class=UserCreationSerializer

    @swagger_auto_schema(operation_summary="Create a User Account")
    def post(self, request):
        data = request.data
        serializer=self.serializer_class(data=request.data)
        if  serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
