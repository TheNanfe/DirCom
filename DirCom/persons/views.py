from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.http import JsonResponse

from django.shortcuts import render

from .serializers import PersonSerializer
from .models import Person


@api_view(['GET'])
def list_persons(request):
    person_list = Person.list_persons(None)
    serializer = PersonSerializer(data=person_list, many=True)
    if serializer.is_valid():
        return Response(serializer.data)
    else:
        print(serializer.errors)
    return Response(status=400)


@api_view(['POST'])
def create_person(request):
    serializer = PersonSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=200)

    return Response(status=400)


@api_view(['POST', 'GET'])
def person_details(request, pk):
    if request.method == 'GET':
        details = Person.get_person(pk)
        serializer = PersonSerializer(data=details, many=True)
        if serializer.is_valid():
            return Response(serializer.data)

    if request.method == 'POST':
        edit_person = Person.objects.get(id=pk)
        edit_serializer = PersonSerializer(instance=edit_person, data=request.data)
        if edit_serializer.is_valid():
            edit_serializer.save()
            return Response(status=200)

    return Response(status=400)


@api_view(['POST'])
def delete_person(request, pk):
    pass