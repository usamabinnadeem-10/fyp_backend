from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class Gallery(models.Model):

    name = models.CharField(max_length=100)
    features = ArrayField(
            models.FloatField(),
            size=2048)
#     timestamp = models.DateTimeField(auto_now_add=True, )
#     lat = models.DecimalField(max_digits=9, decimal_places=6)
#     long = models.DecimalField(max_digits=9, decimal_places=6)

