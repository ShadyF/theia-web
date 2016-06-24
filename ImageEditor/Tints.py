from django.shortcuts import get_object_or_404
from .models import ColorTint


class Tint:
    # TODO: Set to receive custom palette and check filter if exists or custom
    def __init__(self, filter_name):
        filter_model = get_object_or_404(ColorTint, name=filter_name)
        self.filter_to_be_applied = self.make_linear_ramp((filter_model.red, filter_model.green, filter_model.blue))

    def process(self, image):
        image = image.convert('L')  # Converts image into grayscale
        image.putpalette(map(int, self.filter_to_be_applied))  # Applies palette to grayscaled image
        image = image.convert('RGB')  # Converts back to RGB
        return image

    # Taken from http://effbot.org/zone/pil-sepia.htm
    @staticmethod
    def make_linear_ramp(white):
        # putpalette expects [r,g,b,r,g,b,...]
        ramp = []
        r, g, b = white
        for i in range(255):
            ramp.extend((r * i / 255, g * i / 255, b * i / 255))
        return ramp
