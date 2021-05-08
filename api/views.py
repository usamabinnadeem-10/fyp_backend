from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import base64
from PIL import Image
import io

# from ..ai import core

class Query(APIView):


    def post(self, request):

        format, imgstr = request.data['query'].split(';base64,')

        img_decoded = base64.b64decode(imgstr)
        stream = io.BytesIO(img_decoded)
        img = Image.open(stream).convert("RGBA")

        """ this would save the image in the directory """ 
        # img.save('query.png','PNG')

        """ this would show the image but apparently it is not working if the file is large :/  """
        # img.show()

        """ test with this code a bit and see what works best,
            saving 'img' first to local storage and then passing the path to the backend_api 
            OR directly passing the 'img' to the backend_api
            KEEP IN MIND that you would have to delete the stored image once the model has processed it"""

        return Response(
            {
                'message' : 'This is Query View'
            },
            status=status.HTTP_200_OK
        )


