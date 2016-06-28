from PIL import Image
from subprocess import check_output, STDOUT, CalledProcessError
from .models import ColorFilter as color_filer_model
from django.shortcuts import get_object_or_404
from tempfile import NamedTemporaryFile
from math import floor

class FilterManager:
    def __init__(self, filter_name):
        filter_model = get_object_or_404(color_filer_model, name=filter_name)
        self.filter_to_be_applied = filter_model.class_name
        print(self.filter_to_be_applied)

    def process(self, image):
        temp_image = NamedTemporaryFile(mode='w+b')
        image.save(temp_image, format(image.format))
        chosen_filter = globals()[self.filter_to_be_applied](temp_image.name)
        chosen_filter.apply()
        image = Image.open(temp_image)
        return image


class ColorFilter:
    def __init__(self, file_path):
        self.file_path = file_path

    def get_image_size(self):
        image = Image.open(self.file_path)
        width, height = image.size
        image.close()
        return width, height

    def apply(self):
        pass


class Ashes(ColorFilter):
    def apply(self):
        execute_command("convert {filename} -modulate 120,10,100 -fill '#222b6d' -colorize 20\
                     -gamma 0.5 -contrast -contrast {filename}", filename=self.file_path)


class Toaster(ColorFilter):
    def apply(self):
        width, height = self.get_image_size()
        colortone(self.file_path, '#330000', 100, True)

        execute_command('convert {filename} -modulate 150,80,100 -gamma 1.2\
                        -contrast -contrast {filename}',
                        filename=self.file_path)
        apply_viginette(self.file_path, width, height, 'none', 'LavenderBlush3', 1.5)
        apply_viginette(self.file_path, width, height, '#ff9966', 'none', 1.5)


##############################################################
##                    HELPER FUNCTIONS                      ##
##############################################################


def execute_command(command, **kwargs):
    args_format = dict(kwargs.items())
    command = command.format(**args_format)
    try:
        check_output(command, shell=True, stderr=STDOUT)
    except CalledProcessError as e:
        error = e.output
        print(e)
        print('\n')
        print(error)


def colortone(file_path, color, level, apply_negation=True):
    arg0 = level
    arg1 = 100 - level
    negate = '-negate' if apply_negation else ''

    execute_command(
        'convert\
        {filename} -set colorspace RGB\
        \( -clone 0 -fill "{color}" -colorize 100% \)\
        \( -clone 0 -colorspace gray {negate} \)\
        -compose blend -define compose:args={arg0},{arg1} -composite\
        {filename}',
        filename=file_path,
        color=color,
        negate=negate,
        arg0=arg0,
        arg1=arg1
    )


def apply_viginette(file_path, image_width, image_height,
                    color_1='none', color_2='black', crop_factor=1.5):
    crop_x = floor(image_width * crop_factor)
    crop_y = floor(image_height * crop_factor)

    execute_command(
        'convert \
        \( {filename} \) \
        \( -size {crop_x}x{crop_y} radial-gradient:{color_1}-{color_2} -gravity center \
        -crop {width}x{height}+0+0 +repage \) -compose multiply -flatten {filename}',
        filename=file_path,
        width=image_width,
        height=image_height,
        crop_x=crop_x,
        crop_y=crop_y,
        color_1=color_1,
        color_2=color_2
    )
