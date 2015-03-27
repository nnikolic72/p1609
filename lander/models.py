from django.db import models

# Create your models here.
from django.utils.datetime_safe import datetime


class Lander(models.Model):
    """
    Extends Django model class
    """
    def __unicode__(self):
        return self.email

    email = models.EmailField(null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)

    created_at = models.DateTimeField(editable=False)
    updated_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        """ On save, update timestamps """
        if not self.id:
            self.created_at = datetime.today()
        self.updated_at = datetime.today()
        return super(Lander, self).save(*args, **kwargs)