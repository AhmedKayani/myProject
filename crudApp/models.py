from django.db import models

# For the signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Create your models here.

# Model for the CRUD App main page
class Crud(models.Model):
    name = models.CharField(max_length=100)
    networth = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    
# For the latest updates of CRUD operations
class Notification(models.Model):
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

@receiver(post_save, sender=Crud)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(message=f"A new entry {instance} was added.")
    else:
        Notification.objects.create(message=f"Entry {instance} was updated.")

@receiver(post_delete, sender=Crud)
def delete_user_profile(sender, instance, **kwargs):
    Notification.objects.create(message=f"Entry {instance} was deleted.")

