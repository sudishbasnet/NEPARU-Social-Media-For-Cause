from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Notification)
admin.site.register(models.User)
admin.site.register(models.Post)
admin.site.register(models.Comment)
admin.site.register(models.Photo)
admin.site.register(models.Inbox)
admin.site.register(models.Rental)
admin.site.register(models.RentalPhoto)
