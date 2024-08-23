from django.db import models

# Create your models here.


class GetAPI(models.Model):
    api = models.CharField(max_length=100)

    def __str__(self):
        return self.api