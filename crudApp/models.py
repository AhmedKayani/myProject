from django.db import models

# For the signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# For the channel
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


from django.utils import timezone

# Create your models here.

# Model for the CRUD App main page
class Crud(models.Model):
    name = models.CharField(max_length=100)
    networth = models.DecimalField(max_digits=10, decimal_places=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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
    channel_layer = get_channel_layer()
    message = f"A new entry {instance} was added." if created else f"Entry {instance} was updated."
    Notification.objects.create(message=message)
    async_to_sync(channel_layer.group_send)(
        'notifications',
        {
            'type': 'send_notification',
            'message': message
        }
    )


@receiver(post_delete, sender=Crud)
def delete_user_profile(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    message = f"Entry {instance} was deleted."
    Notification.objects.create(message=message)
    async_to_sync(channel_layer.group_send)(
        'notifications',
        {
            'type': 'send_notification',
            'message': message
        }
    )

