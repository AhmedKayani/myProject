from django.contrib import admin
from .models import Crud
# Register your models here.

# Registering the CRUD model in the admin panel
admin.site.register(Crud)