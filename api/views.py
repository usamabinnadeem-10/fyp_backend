from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import base64
from PIL import Image
import io

from ..ai import core

class Query(APIView):


    def post(self, request):

        format, imgstr = request.data['query'].split(';base64,')

        img_decoded = base64.b64decode(imgstr)
        stream = io.BytesIO(img_decoded)
        img = Image.open(stream).convert("RGBA")
        img.show()
        
        return Response(
            {
                'message' : 'This is Query View'
            },
            status=status.HTTP_200_OK
        )


