from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view

from note.models import Note
from note.serializers import NoteSerializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Create your views here.
@api_view(['GET'])
def notes_list(request):
    
    if request.method == 'GET':
        userId = request.GET.get('user', None)
        if userId == None:
            return JsonResponse({'message' : 'Please login first'}, status=status.HTTP_403_FORBIDDEN)
        
        user = User.objects.get(id=int(userId))
        if not user:
            return JsonResponse({'message' : 'User does not exists'}, status=status.HTTP_404_NOT_FOUND)


        notes = Note.objects.filter(author = user)
    
        notes_serializar = NoteSerializers(notes, many=True)
        return JsonResponse(notes_serializar.data, safe=False)


@api_view(['POST'])
def create_note(request):

    if request.method == 'POST':

        userId = request.GET.get('user', None)
        if userId == None:
            return JsonResponse({'message' : 'Please login first'}, status=status.HTTP_403_FORBIDDEN)
        
        user = User.objects.get(id=int(userId))
        if not user:
            return JsonResponse({'message' : 'User does not exists'}, status=status.HTTP_404_NOT_FOUND)

        notes_data = JSONParser().parse(request)
        notes_serializar = NoteSerializers(data=notes_data)

        if notes_serializar.is_valid():
            notes_serializar.save(author = user)
            return JsonResponse({"status" : "success"}, status=status.HTTP_201_CREATED)

        return JsonResponse(notes_serializar.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def user_login(request):

    if request.method == 'POST':
        username = request.data.get("username", None)
        password = request.data.get("password", None)
        
        if not username or not password:
            return JsonResponse({'message' : 'Incomplete Data'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(username = username)
            if user.check_password(password):
                return JsonResponse({'status' : "success", "userId" : user.id}, status=status.HTTP_200_OK)

            return JsonResponse({'message' : 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return JsonResponse({'message' : 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def user_register(request):

    if request.method == 'POST':
        username = request.data.get("username", None)
        password = request.data.get("password", None)
        
        if not username or not password:
            return JsonResponse({'message' : 'Incomplete Data'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username = username)
            return JsonResponse({'message' : 'User alredy exits.'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            user = User.objects.create_user(username = username, password = password)
            user.save()
            return JsonResponse({'status': 'Account Created'}, status=status.HTTP_200_OK)
            