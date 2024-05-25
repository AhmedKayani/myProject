from django.db import models

# Create your models here.

# Model for the CRUD App main page
class Crud(models.Model):
    name = models.CharField(max_length=100)
    networth = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name