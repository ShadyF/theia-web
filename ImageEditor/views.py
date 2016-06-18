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

    def dispatch(self, request, *args, **kwargs):
        self.func_dict = {"sharpen": self.sharpen}
        return super(Editor, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        image_bytes = self.decode_base64_image(request.POST.get('imgBase64'))

        # Open image using Pillow
        image = Image.open(image_bytes)

        # Call approriate function corresponding to action attr from ajax call
        im = self.func_dict[request.POST.get('action')](image)

        # Encode the image back again to base64
        encoded_image = self.encode_base64_image(im)
        image.close()

        # return json to ajax call
        return JsonResponse({'processed_image': encoded_image})

    @staticmethod
    def sharpen(im):
        return im.filter(ImageFilter.SHARPEN())

    @staticmethod
    def decode_base64_image(base64_string):
        img_data = re.sub('^data:image/.+;base64,', '', base64_string)
        return BytesIO(base64.b64decode(img_data))

    @staticmethod
    def encode_base64_image(image):
        buffered_image = BytesIO()
        image.save(buffered_image, format("JPEG"))
        return 'data:image/jpg;base64,' + base64.b64encode(buffered_image.getvalue()).decode()
