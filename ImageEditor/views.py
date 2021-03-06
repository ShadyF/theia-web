import mimetypes
import re

import sys
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.http import JsonResponse, Http404, StreamingHttpResponse
from wsgiref.util import FileWrapper

from .Transformations import *
from .Tints import Tint
from .Enhancements import *
from .KernelFilters import KernelFilterApplier
from .ColorFilters import FilterManager
from .models import ColorTint, ColorFilter, KernelFilter, ImageFunction

from io import BytesIO
from PIL import Image
from base64 import b64encode, b64decode


class Editor(View):
    template_name = 'ImageEditor/editor.html'

    def get(self, request):
        color_tints = ColorTint.objects.all()
        color_filters = ColorFilter.objects.all()
        kernel_filters = KernelFilter.objects.all()
        adjustments = ImageFunction.objects.filter(function_type='Adjustment')
        transforms = ImageFunction.objects.filter(function_type='Transform')
        context = {'color_tints': color_tints, 'adjustments': adjustments,
                   'color_filters': color_filters, 'transforms': transforms,
                   'kernel_filters': kernel_filters}
        return render(request, self.template_name, context)


class ImageOperation(View):
    def post(self, request, operation_type):
        class_dict = self.get_class_dict()  # Get dict of all available operations

        if operation_type not in class_dict:  # Raise 404 if invalid operation
            raise Http404

        # If the last operation is not the same as the last one, get an the update image from the canvas
        # and store it in the user's current session

        # If the last operation was the same as the current one, edit the previously saved image
        # This solves the scenario where the user is testing out different values of sharpness, for examaple
        # as updating the image for each harpness change would cause the sharpness enhancement to be applied to
        # a previously sharpened image.
        if request.session.get('LAST_OPERATION') != operation_type:
            request.session['LAST_OPERATION'] = operation_type
            image_base64 = request.session.get('current_image_base64')
            request.session['pre_operation_image_base64'] = image_base64

        else:
            image_base64 = request.session.get('pre_operation_image_base64')

        image_bytes = self.decode_base64_image(image_base64)
        image = Image.open(image_bytes)

        # Instantiate the approrpriate image operation
        class_to_instantiate = get_object_or_404(ImageFunction, display_name=operation_type).class_name
        operation = class_dict[class_to_instantiate](request.POST.get('params'))

        # process the current image
        output_image = operation.process(image)
        output_image_base64 = self.encode_base64_image(output_image)
        request.session['current_image_base64'] = output_image_base64

        image.close()

        return JsonResponse({'processed_image': output_image_base64})

    @staticmethod
    def decode_base64_image(base64_string):
        # Remove the "data:image/jpg;base64," tag at the beginning of the string
        # Would lead to a corrupted image otherwise
        # reg = re.compile("data:image/(.*?);")
        # self.format = reg.match(base64_string[:25]).group(1)
        img_data = re.sub('^data:image/.+;base64,', '', base64_string)
        return BytesIO(b64decode(img_data))

    @staticmethod
    def encode_base64_image(image):
        buffered_image = BytesIO()
        image.save(buffered_image, format('JPEG'))
        return 'data:image/jpeg;base64,' + b64encode(buffered_image.getvalue()).decode()

    @staticmethod
    def get_class_dict():
        """Return a dict of all the available classes in the global namespace"""
        class_dict = globals()
        return class_dict


class ImageUploadHandler(View):
    def post(self, request):
        request.session['LAST_OPERATION'] = ""
        request.session['original_image_base64'] = request.POST['imgBase64']
        request.session['pre_operation_image_base64'] = request.POST['imgBase64']
        request.session['current_image_base64'] = request.POST['imgBase64']
        request.session.set_expiry(0)

        return JsonResponse({"OK": "IT WORKS"})


def reset_image(request):
    if request.method == 'POST':
        try:
            original_image = request.session.get('original_image_base64')
        except KeyError:
            raise Http404("Image could not be reset")

        request.session['pre_operation_image_base64'] = original_image
        request.session['current_image_base64'] = original_image

        return JsonResponse({'processed_image': original_image})


def download_image(request):
    if request.method == 'GET':
        try:
            decoded_image = ImageOperation.decode_base64_image(request.session['current_image_base64'])
        except KeyError:
            raise Http404("No image to download")
        chunk_size = 8192
        response = StreamingHttpResponse(FileWrapper(decoded_image, chunk_size),
                                         content_type='image/jpeg')
        response['Content-Disposition'] = "attachment; filename=image-download.jpeg"
        return response
