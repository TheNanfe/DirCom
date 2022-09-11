from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


# Create your views here.


@api_view(['GET'])
def list_users(request):
    users = User.objects.all()
    serializer = UserSerializer(data=users, many=False)
    if serializer.is_valid():
        return Response(serializer.data)
    return Response(status=400)


@api_view(['GET', 'POST'])
def get_user(request, pk):
    if request.method == 'GET':
        user = User.objects.get(id=pk)
        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)

    if request.method == 'POST':
        user = User.objects.get(id=pk)
        serializer = UserSerializer(instance=user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

    return Response(status=400)


@api_view(['POST'])
def create_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=200)

    return Response(status=400)


@api_view(['POST'])
def delete_user(request, pk):
    user_delete = User.status_change('DELETE', pk)
    if user_delete is not None:
        return JsonResponse({'message': 'El usuario con ha sido modificado exitosamente!', 'type': 'success'})
    return JsonResponse({'message': 'El usuario no se ha podido modificar', 'type': 'error'})
