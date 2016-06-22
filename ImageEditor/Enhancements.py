from PIL import ImageEnhance


class Enhancement:
    # TODO: add try catch block here when converting to float
    def __init__(self, value_string="1.0"):
        self.value = float(value_string)

    def adjust(self, image):
        return image

    def process(self, image):
        # if self.value != 1.0:
        return self.adjust(image)


class Sharpness(Enhancement):
    def adjust(self, image):
        return ImageEnhance.Sharpness(image).enhance(self.value)


class Brightness(Enhancement):
    def adjust(self, image):
        return ImageEnhance.Brightness(image).enhance(self.value)


class Contrast(Enhancement):
    def adjust(self, image):
        return ImageEnhance.Contrast(image).enhance(self.value)


class Color(Enhancement):
    def adjust(self, image):
        return ImageEnhance.Color(image).enhance(self.value)
