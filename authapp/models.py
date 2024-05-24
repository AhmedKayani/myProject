from django.db import models

# Model for the user profile which is the name of the person and their networth
class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    networth = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name