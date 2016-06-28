from PIL import Image
from subprocess import check_output, STDOUT
from .models import ColorFilter as color_filer_model
from django.shortcuts import get_object_or_404
from tempfile import NamedTemporaryFile

class FilterManager:
    def __init__(self, filter_name):
        filter_model = get_object_or_404(color_filer_model, name=filter_name)
        self.filter_to_be_applied = filter_model.class_name
        print(self.filter_to_be_applied)

    def process(self, image):
        temp_image = NamedTemporaryFile(mode='w+b')
        image.save(temp_image, format(image.format))
        chosen_filter = globals()[self.filter_to_be_applied]()
        chosen_filter.apply(temp_image.name)
        image = Image.open(temp_image)
        return image


class ColorFilter:
    def execute(self, command, **kwargs):
        format = dict(kwargs.items())
        command = command.format(**format)
        error = check_output(command, shell=True, stderr=STDOUT)
        return error

    def colortone(self, color, level, apply_negation=True):
        arg0 = level
        arg1 = 100 - level
        negate = '-negate' if apply_negation else ''

        self.execute(
            "convert {filename} \
            ( -clone 0 -fill '{color}' -colorize 100% \) \
            ( -clone 0 -colorspace gray {negate})\
             -compose blend -define compose:args={arg0},{arg1} -composite {filename}",
            color=color,
            negate=negate,
            arg0=arg0,
            arg1=arg1
        )


class Ashes(ColorFilter):
    def apply(self, file_path):
        self.execute("convert {filename} -modulate 120,10,100 -fill '#222b6d' -colorize 20\
                     -gamma 0.5 -contrast -contrast {filename}", filename=file_path)
