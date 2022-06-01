from django.http import HttpResponse
from django.shortcuts import render
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from azure.storage.blob import BlobServiceClient, BlobClient

from .serializers import GoogleUserSerializer
from .models import GoogleUser
from .test_db import add_image_db, get_gallery, add_user, remove_image_db


import requests


class GoogleUserViewSet(viewsets.ModelViewSet):
    queryset = GoogleUser.objects.all().order_by('name')
    serializer_class = GoogleUserSerializer

@api_view(['POST'])
def google_login(request):
    if request.method == 'POST':
        received_data = JSONParser().parse(request)
        token = received_data[0]
        google_login_data = received_data[1]
        google_login_data_serializer = GoogleUserSerializer(data=google_login_data)

        oauth_url = 'https://oauth2.googleapis.com/tokeninfo'
        token_obj = {'access_token': token}

        oauth_request = requests.post(oauth_url, data=token_obj)

        # if google_login_data_serializer.is_valid():
        #     google_login_data_serializer.save()

        if(oauth_request.status_code == 200):
            add_user(received_data[1])
            return(HttpResponse(status=200))
        else:
            return(HttpResponse(status=401))

@api_view(['POST'])
def galery_pull(request):
    if request.method == 'POST':
        received_data = JSONParser().parse(request)
        google_id = received_data[0]
        data = get_gallery(google_id)
        if(data):
            return(data)
        else:
            return(HttpResponse(status=204))

@api_view(['POST'])
def new_user(request):
    if request.method == 'POST':
        received_data = JSONParser().parse(request)
        add_user(received_data)
        return(HttpResponse(status=200))

def move_delete_blob(name):
    account_key = 'YKMIcV8GQklYxOvuSN14c4pXsysf+b3sM5kydvrug5BBwGARNtWmpx59dee9RuFSjA4D4XNA+NLP+AStFWO9Dg==' # The account key for the source container
    blob_service = BlobServiceClient(account_url='https://imagesstoragesuperhero.blob.core.windows.net/', credential=account_key) 
    source_container_name = 'generatedimages' # Name of container which has blob to be copied
    blob_name = name # Name of the blob you want to copy
    destination_container_name = 'savedimages' # Name of container where blob will be copied

    source_blob = BlobClient(
        'https://imagesstoragesuperhero.blob.core.windows.net/',
        container_name = source_container_name, 
        blob_name = blob_name,
        credential = account_key
    )

    new_blob = blob_service.get_blob_client(destination_container_name, blob_name)    
    new_blob.start_copy_from_url(source_blob.url)
    source_blob.delete_blob()

def delete_blob(name):
    account_key = 'YKMIcV8GQklYxOvuSN14c4pXsysf+b3sM5kydvrug5BBwGARNtWmpx59dee9RuFSjA4D4XNA+NLP+AStFWO9Dg==' # The account key for the source container
    # blob_service = BlobServiceClient(account_url='https://imagesstoragesuperhero.blob.core.windows.net/', credential=account_key) 
    source_container_name = 'savedimages' # Name of container which has blob to be copied
    blob_name = name # Name of the blob you want to copy

    source_blob = BlobClient(
        'https://imagesstoragesuperhero.blob.core.windows.net/',
        container_name = source_container_name, 
        blob_name = blob_name,
        credential = account_key
    )

    source_blob.delete_blob()

@api_view(['POST'])
def add_image(request):
    if request.method == 'POST':
        received_data = JSONParser().parse(request)
        add_image_db(received_data)
        move_delete_blob(received_data['imgName'])
        return(HttpResponse(status=200))

@api_view(['POST'])
def remove_image(request):
    if request.method == 'POST':
        received_data = JSONParser().parse(request)
        remove_image_db(received_data)
        delete_blob(received_data['imgName'])
        return(HttpResponse(status=200))