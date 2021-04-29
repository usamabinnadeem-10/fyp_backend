from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Create your views here.
class Query(APIView):


    def post(self, request):
        return Response(
            {
                'message' : 'This is Query View'
            },
            status=status.HTTP_200_OK
        )


