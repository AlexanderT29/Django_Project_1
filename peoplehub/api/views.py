from django.shortcuts import render
from .models import Person
from .serializers import PersonSerializer
from rest_framework.renderers import JSONRenderer
from django.http import HttpResponse
import io
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from rest_framework import status
from django.shortcuts import get_object_or_404

@csrf_exempt
def singleobj(request, id):
    data = get_object_or_404(Person, id=id)
    if request.method == 'PUT':
        stream = io.BytesIO(request.body)
        parsed_data = JSONParser().parse(stream)
        serializer = PersonSerializer(data, data=parsed_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'update':'success'})
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'PATCH':
        stream = io.BytesIO(request.body)
        parsed_data = JSONParser().parse(stream)
        serializer = PersonSerializer(data, data=parsed_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'update':'success'})
    serializer = PersonSerializer(data)
    return JsonResponse(serializer.data)
    

@csrf_exempt
def multipleobj(request):
    if request.method == "POST":
        json = request.body
        stream = io.BytesIO(json)
        parsed_data = JSONParser().parse(stream)
        serializer = PersonSerializer(data=parsed_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"created":"successfull"}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    data = Person.objects.all()
    serializer = PersonSerializer(data, many=True)
    return JsonResponse(serializer.data, safe=False)