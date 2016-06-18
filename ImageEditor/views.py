from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse

from io import BytesIO, StringIO
from PIL import Image
from PIL import ImageFilter
import base64
import re

class Editor(View):
    template_name = 'ImageEditor/editor.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        img_data = request.POST.get('imgBase64')
        img_data = re.sub('^data:image/.+;base64,', '', img_data)
        im = Image.open(BytesIO(base64.b64decode(img_data)))
        im = im.filter(ImageFilter.GaussianBlur(5))
        buffered_image = BytesIO()
        im.save(buffered_image, format("JPEG"))
        out_data = 'data:image/jpg;base64,' + base64.b64encode(buffered_image.getvalue()).decode()
        im.close()
        return JsonResponse({'img': out_data})
