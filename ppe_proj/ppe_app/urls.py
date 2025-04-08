from django.urls import path
from .views import detect_ppe, upload_page# Import your view function

urlpatterns = [    path('',  upload_page, name='detect_ppe'),  # Define endpoint

            path('detect_ppe/', detect_ppe, name='detect_ppe'),  # Define endpoint

      
]
from django.shortcuts import render
