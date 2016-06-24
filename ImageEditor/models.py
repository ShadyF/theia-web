from django.db import models


class ColorTint(models.Model):
    name = models.CharField(max_length=15)
    red = models.IntegerField(default=0)
    green = models.IntegerField(default=0)
    blue = models.IntegerField(default=0)

    def __str__(self):
        return self.name + " (" + str(self.red) + ", " + str(self.green) + ", " + str(self.blue) + ")"
