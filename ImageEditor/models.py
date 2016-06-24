from django.db import models


class ColorTint(models.Model):
    name = models.CharField(max_length=15)
    red = models.IntegerField(default=0)
    green = models.IntegerField(default=0)
    blue = models.IntegerField(default=0)

    def __str__(self):
        return self.name + " (" + str(self.red) + ", " + str(self.green) + ", " + str(self.blue) + ")"


class ImageFunction(models.Model):
    FUNCTION_TYPES = (
        ('Transform', 'Transform'),
        ('Tint', 'Color Tint'),
        ('Adjustment', 'Adjustment'),
        ('ColorFilter', 'Color Filter'),
        ('KernelFilter', 'Kernel Filter')
    )
    display_name = models.CharField(max_length=30, unique=True)
    class_name = models.CharField(max_length=30)
    function_type = models.CharField(max_length=15, choices=FUNCTION_TYPES)

    def __str__(self):
        return "[" + self.function_type + "] " + "'" + self.display_name + "': " + self.class_name

        # class Meta:
        #     abstract = True

# class TransformFunction(ImageFunction):
#     pass
#
#
# class ColorFilterFunction(ImageFunction):
#     pass
#
#
# class KernelFilterFunction(ImageFunction):
#     pass
