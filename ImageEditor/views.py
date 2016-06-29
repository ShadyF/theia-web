from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.http import JsonResponse, Http404

from .Transformations import *
from .Tints import Tint
from .Enhancements import *
from .KernelFilters import *
from .ColorFilters import FilterManager
from .models import ColorTint, ColorFilter, ImageFunction

import re
from io import BytesIO
from PIL import Image
from base64 import b64encode, b64decode

LAST_OPERATION = ""


class Editor(View):
    template_name = 'ImageEditor/editor.html'

    def get(self, request):
        color_tints = ColorTint.objects.all()
        color_filters = ColorFilter.objects.all()
        adjustments = ImageFunction.objects.filter(function_type='Adjustment')
        transforms = ImageFunction.objects.filter(function_type='Transform')
        kernel_filters = ImageFunction.objects.filter(function_type='KernelFilter')
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
        global LAST_OPERATION
        if LAST_OPERATION != operation_type:
            LAST_OPERATION = operation_type
            request.session['current_image_base64'] = request.POST.get('imgBase64')

        image_base64 = request.session.get('current_image_base64')
        image_bytes = self.decode_base64_image(image_base64)
        image = Image.open(image_bytes)

        # Instantiate the approrpriate image operation
        class_to_instantiate = get_object_or_404(ImageFunction, display_name=operation_type).class_name
        operation = class_dict[class_to_instantiate](request.POST['params'])

        # process the current image
        output_image = operation.process(image)
        output_image_base64 = self.encode_base64_image(output_image, self.format)

        image.close()

        return JsonResponse({'processed_image': output_image_base64})

    def decode_base64_image(self, base64_string):
        # Remove the "data:image/jpg;base64," tag at the beginning of the string
        # Would lead to a corrupted image otherwise
        reg = re.compile("data:image/(.*?);")
        self.format = reg.match(base64_string[:25]).group(1)
        img_data = re.sub('^data:image/.+;base64,', '', base64_string)
        return BytesIO(b64decode(img_data))

    @staticmethod
    def encode_base64_image(image, image_format):
        buffered_image = BytesIO()
        image.save(buffered_image, format(image_format))
        return 'data:image/' + image_format + ';base64,' + b64encode(buffered_image.getvalue()).decode()

    @staticmethod
    def get_class_dict():
        """Return a dict of all the available classes in the global namespace"""
        class_dict = globals()
        return class_dict


class ImageUploadHandler(View):
    def post(self, request):
        request.session['original_image_base64'] = request.POST['imgBase64']
        request.session['current_image_base64'] = request.POST['imgBase64']
        request.session.set_expiry(0)

        return JsonResponse({"OK": "IT WORKS"})


def reset_image(request):
    if request.method == 'POST':
        try:
            original_image = request.session['original_image_base64']
        except KeyError:
            raise Http404("Image could not be reset")

        request.session['current_image_base64'] = original_image
        return JsonResponse({'processed_image': original_image})
