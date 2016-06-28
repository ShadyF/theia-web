from PIL import Image
from subprocess import check_output, STDOUT, CalledProcessError
from .models import ColorFilter as ColorFilterModel
from django.shortcuts import get_object_or_404
from tempfile import NamedTemporaryFile
from math import floor


class FilterManager:
    def __init__(self, filter_name):
        filter_model = get_object_or_404(ColorFilterModel, name=filter_name)
        self.filter_to_be_applied = filter_model.class_name
        print(self.filter_to_be_applied)

    def process(self, image):
        temp_image = NamedTemporaryFile(mode='w+b')
        image.save(temp_image, format(image.format))
        chosen_filter = globals()[self.filter_to_be_applied](temp_image.name, image.size[0], image.size[1])
        chosen_filter.apply()
        image = Image.open(temp_image)
        return image


class ColorFilter:
    def __init__(self, file_path, width, height):
        self.file_path = file_path
        self.width = width
        self.height = height

    def colortone(self, color, level, apply_negation=True):
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
            filename=self.file_path,
            color=color,
            negate=negate,
            arg0=arg0,
            arg1=arg1
        )

    def apply_viginette(self, inner_color='none', outer_color='black', crop_factor=1.5):
        crop_x = floor(self.width * crop_factor)
        crop_y = floor(self.height * crop_factor)
        execute_command(
            'convert \
            \( {filename} \) \
            \( -size {crop_x}x{crop_y} radial-gradient:{color_1}-{color_2} -gravity center \
            -crop {width}x{height}+0+0 +repage \) -compose multiply -flatten {filename}',
            filename=self.file_path,
            width=self.width,
            height=self.height,
            crop_x=crop_x,
            crop_y=crop_y,
            color_1=inner_color,
            color_2=outer_color
        )

    def apply(self):
        pass


class Ashes(ColorFilter):
    def apply(self):
        execute_command("convert {filename} -modulate 120,10,100 -fill '#222b6d' -colorize 20\
                     -gamma 0.5 -contrast -contrast {filename}", filename=self.file_path)


class Toaster(ColorFilter):
    def apply(self):
        self.colortone('#330000', 100, True)

        execute_command('convert {filename} -modulate 150,80,100 -gamma 1.2\
                        -contrast -contrast {filename}',
                        filename=self.file_path)
        self.apply_viginette('none', 'LavenderBlush3', 1.5)
        self.apply_viginette('#ff9966', 'none', 1.5)


class SummerTouch(ColorFilter):
    def apply(self):
        self.colortone('#222b6d', 100, True)  # Change blacks to indigo
        self.colortone('#f7daae', 100, False)  # Change whites to peach

        execute_command('convert {filename} -contrast -modulate 100,150,100\
                        -auto-gamma {filename}', filename=self.file_path)


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
