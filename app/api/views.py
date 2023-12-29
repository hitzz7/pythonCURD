

# Create your views here.
from django.contrib.auth.hashers import make_password
from ..models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .serializer import UserSerilizer 


@api_view(['GET'])
def eventlist(request):
    queryset=User.objects.all()
    serializer=UserSerilizer(queryset,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def eventdetail(request,pk):
    try:
        queryset=User.objects.get(id=pk)
        serializer=UserSerilizer(queryset,many=False)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response('id not found', status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def eventcreate(request):
    
    serializer=UserSerilizer(data=request.data)
    
    if serializer.is_valid():
        password = serializer.validated_data.get('password')
        hashed_password = make_password(password)
        serializer.validated_data['password'] = hashed_password
        serializer.save()
    else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.data)

@api_view(['PUT'])
def eventupdate(request,pk):
    try:
        queryset=User.objects.get(id=pk)
        serializer=UserSerilizer(instance=queryset,data=request.data)
    
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    except User.DoesNotExist:
        return Response('id not found', status=status.HTTP_404_NOT_FOUND)
    


@api_view(['DELETE'])
def eventdelete(request, pk):
    try:
        user = get_object_or_404(User, id=pk)
        user.delete()
        return Response('Item deleted successfully', status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response('id not found', status=status.HTTP_404_NOT_FOUND)


