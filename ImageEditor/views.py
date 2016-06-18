from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse

from io import BytesIO, StringIO
from PIL import Image
from PIL import ImageFilter
import base64
import re
from urllib.parse import parse_qs

class Editor(View):
    template_name = 'ImageEditor/editor.html'

    def dispatch(self, request, *args, **kwargs):
        self.func_dict = {"Sharpen": self.sharpen, "Blur": self.blur,
                          "EdgeEnhance": self.edgeEnhance, "Translate": self.translate}
        return super(Editor, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        image_bytes = self.decode_base64_image(request.POST.get('imgBase64'))

        # Open image using Pillow
        image = Image.open(image_bytes)

        # Call approriate function corresponding to action attr from ajax call
        try:
            im = self.func_dict[request.POST.get('action')](image, request.POST.get('params'))
        except TypeError:
            im = self.func_dict[request.POST.get('action')](image)
        except:
            im = image
        # Encode the image back again to base64
        encoded_image = self.encode_base64_image(im)
        image.close()

        # return json to ajax call
        return JsonResponse({'processed_image': encoded_image})

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
