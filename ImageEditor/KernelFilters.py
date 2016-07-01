from django.shortcuts import get_object_or_404
from .models import KernelFilter as KernelFilterModel
from PIL import ImageFilter


class KernelFilterApplier:
    def __init__(self, filter_name):
        filter_model = get_object_or_404(KernelFilterModel, name=filter_name)
        self.filter_to_be_applied = filter_model.class_name

    def process(self, image):
        chosen_filter = globals()[self.filter_to_be_applied]()
        return chosen_filter.apply(image)


class KernelFilter:
    def apply(self, image):
        return image


class Blur(KernelFilter):
    def apply(self, image):
        return image.filter(ImageFilter.BLUR)


class Contour(KernelFilter):
    def apply(self, image):
        return image.filter(ImageFilter.CONTOUR)


class Detail(KernelFilter):
    def apply(self, image):
        return image.filter(ImageFilter.DETAIL)


class EdgeEnhance(KernelFilter):
    def apply(self, image):
        return image.filter(ImageFilter.EDGE_ENHANCE)


class Emboss(KernelFilter):
    def apply(self, image):
        return image.filter(ImageFilter.EMBOSS)


class FindEdges(KernelFilter):
    def apply(self, image):
        return image.filter(ImageFilter.FIND_EDGES)


class Smooth(KernelFilter):
    def apply(self, image):
        return image.filter(ImageFilter.SMOOTH)


class Sharpen(KernelFilter):
    def apply(self, image):
        return image.filter(ImageFilter.SHARPEN)
