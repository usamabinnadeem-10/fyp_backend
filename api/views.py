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

        feats = Gallery.objects.values_list('features',flat=True)

        core = Core()
        core.load_gallery_feats(feats)

        format, imgstr = request.data['query'].split(';base64,')
        img_decoded = base64.b64decode(imgstr)
        stream = io.BytesIO(img_decoded)
        img = Image.open(stream).convert("RGB")

        results = core.run(query=img)
        result_images = []

        for result in results[0]:
            instance = Gallery.objects.get(pk=result+1)
            result_images.append(instance.name)

        return Response(
            {
                'result' : result_images
            },
            status=status.HTTP_200_OK
        )


