from django.shortcuts import render
from .models import Person
from .serializers import PersonSerializer, PersonModelSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
import io
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import CreateModelMixin, ListModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView
from rest_framework.authentication import TokenAuthentication

@api_view(['GET','PUT','PATCH'])
def singleobj(request, id):
    data = get_object_or_404(Person, id=id)
    if request.method == 'PUT':
        parsed_data = request.data
        serializer = PersonModelSerializer(data, data=parsed_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'update':'success'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'PATCH':
        parsed_data = request.data
        serializer = PersonModelSerializer(data, data=parsed_data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'update':'success'})
    if request.method == 'GET':
        serializer = PersonModelSerializer(data)
        return Response(serializer.data)
    
    

@api_view(['GET','POST'])
def multipleobj(request):
    if request.method == "POST":
        parsed_data = request.data
        serializer = PersonModelSerializer(data=parsed_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"created":"successfull"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        print(request.accepted_renderer)
        data = Person.objects.all()
        serializer = PersonModelSerializer(data, many=True)
        return Response(serializer.data)
    
class multipleObjAPIView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    queryset = Person.objects.all()
    serializer_class = PersonModelSerializer

    def get(self, request, *args, **kwargs):
        print(request.user)
        response = super().get(request, *args, **kwargs)

        return response
    
    
class singleObjAPIView(RetrieveUpdateAPIView):
    queryset = Person.objects.all()
    serializer_class = PersonModelSerializer