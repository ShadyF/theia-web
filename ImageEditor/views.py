from django.shortcuts import get_object_or_404, render
from django.views.generic import View
from django.http import JsonResponse
from .models import ColorFilter

from io import BytesIO
from PIL import Image
from PIL import ImageFilter
import base64
import re
from urllib.parse import parse_qs

last_operation = ""


class Editor(View):
    template_name = 'ImageEditor/editor.html'

    def dispatch(self, request, *args, **kwargs):
        self.func_dict = {"Sharpen": self.sharpen, "Blur": self.blur,
                          "EdgeEnhance": self.edgeEnhance, "Translate": self.translate,
                          }
        return super(Editor, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        filters = ColorFilter.objects.all()
        context = {'filters': filters}
        return render(request, self.template_name, context)

    def post(self, request):
        # if request.POST.get('save') == 'true':
        request.session['image'] = request.POST['imgBase64']
        request.session.set_expiry(0)

        #image_bytes = self.decode_base64_image(request.session['image'])
        # Open image using Pillow
        #image = Image.open(image_bytes)
        # Call approriate function corresponding to action attr from ajax call
        # try:
        #    im = self.func_dict[request.POST.get('action')](image, request.POST.get('params'))
        # except TypeError:
        #    im = self.func_dict[request.POST.get('action')](image)
        # except:
        #    im = image
        # Encode the image back again to base64
        # encoded_image = self.encode_base64_image(im)
        #image.close()

        # return json to ajax call
        # return JsonResponse({'processed_image': encoded_image})
        return JsonResponse({'processed_image': "OK"})

    @staticmethod
    def sharpen(im):
        return im.filter(ImageFilter.SHARPEN())
        # To scale down image
        # im.thumbnail((1200, 1200), Image.ANTIALIAS)
        # return im

    @staticmethod
    def blur(im):
        return im.filter(ImageFilter.BLUR)

    @staticmethod
    def edgeEnhance(im):
        return im.filter(ImageFilter.EDGE_ENHANCE)

    # need to be sped up
    # crop and paste?
    @staticmethod
    def translate(im, params):
        params = parse_qs(params)
        print(params['X'])
        dx = int(params['X'][0])
        dy = int(params['Y'][0])
        x_size = im.size[0]
        y_size = im.size[1]
        curr = im.load()
        new_img = Image.new('RGB', (x_size, y_size))
        for x in range(x_size):
            for y in range(y_size):
                rgb_val = curr[x, y]
                x_new = x + dx
                y_new = y + dy

                if x_new in range(x_size) and y_new in range(y_size):
                    new_img.putpixel((x_new, y_new), rgb_val)

        return new_img

    @staticmethod
    def decode_base64_image(base64_string):
        img_data = re.sub('^data:image/.+;base64,', '', base64_string)
        return BytesIO(base64.b64decode(img_data))

    @staticmethod
    def encode_base64_image(image):
        buffered_image = BytesIO()
        image.save(buffered_image, format("JPEG"))
        return 'data:image/jpg;base64,' + base64.b64encode(buffered_image.getvalue()).decode()


def decode_base64_image(base64_string):
    img_data = re.sub('^data:image/.+;base64,', '', base64_string)
    return BytesIO(base64.b64decode(img_data))


def encode_base64_image(image):
    buffered_image = BytesIO()
    image.save(buffered_image, format("JPEG"))
    return 'data:image/jpg;base64,' + base64.b64encode(buffered_image.getvalue()).decode()


def apply_color_filter(request, filter_name):
    if request.method == 'POST':
        filter_model = get_object_or_404(ColorFilter, name=filter_name)
        filter_to_be_applied = make_linear_ramp((filter_model.red, filter_model.green, filter_model.blue))

        if last_operation != 'filter':  # try block here
            request.session['image'] = request.POST.get('imgBase64')

        image_bytes = decode_base64_image(request.session['image'])
        image = Image.open(image_bytes).convert('L')
        image.putpalette(map(int, filter_to_be_applied))
        image = image.convert("RGB")
        encoded_image = encode_base64_image(image)
        image.close()
        return JsonResponse({'processed_image': encoded_image})
        # else
        # raise 404


def make_linear_ramp(white):
    # putpalette expects [r,g,b,r,g,b,...]
    ramp = []
    r, g, b = white
    for i in range(255):
        ramp.extend((r * i / 255, g * i / 255, b * i / 255))
    return ramp
