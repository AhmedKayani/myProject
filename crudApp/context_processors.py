from .models import Notification

# To show the latest notification on top of the page.
def latest_notification(request):
    latest_notification = Notification.objects.all().order_by('-timestamp').first()
    return {
        'latest_notification': latest_notification
    }

