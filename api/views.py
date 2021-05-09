from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import base64
from PIL import Image
import io

from ai.core import Core
from .models import Gallery

class Query(APIView):

    def post(self, request):

        feats = Gallery.objects.values_list('features')

        print(type(feats))
        print(type(feats[0]))
        print(len(feats))
        print(len(feats[0][0]))

        core = Core()
        core.load_gallery_feats(feats)

        format, imgstr = request.data['query'].split(';base64,')
        img_decoded = base64.b64decode(imgstr)
        stream = io.BytesIO(img_decoded)
        img = Image.open(stream).convert("RGBA")

        result = core.run(query=img)
        
    
        # img.save('query.png','PNG')

        # img.show()


        return Response(
            {
                'message' : 'This is Query View'
            },
            status=status.HTTP_200_OK
        )


