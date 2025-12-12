from django.contrib import admin
from .models import (Notification, NotificationRecipient)
# Register your models here.

admin.site.register(Notification),
admin.site.register(NotificationRecipient)