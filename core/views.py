from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# Create your views here.

class ContactView(APIView):

    def post(self, request, format=None):

        return Response({"data":"data"}, status=status.HTTP_200_OK)
    
class DealView(APIView):

    def post(self, request, format=None):

        return Response({"data":"data"}, status=status.HTTP_200_OK)
    
class AssociateView(APIView):

    def get(self, request, format=None):

        return Response({"data":"data"}, status=status.HTTP_200_OK)
    def post(self, request, format=None):

        return Response({"data":"data"}, status=status.HTTP_200_OK)