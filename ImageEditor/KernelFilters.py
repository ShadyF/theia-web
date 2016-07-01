from PIL import ImageFilter


class KernelFilterApllier:
    def __init__(self):
        pass


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
