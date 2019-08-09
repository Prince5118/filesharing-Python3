
from django.contrib import admin

# Register your models here.
from .models import File,User,SharedRecord

admin.site.register(File)
admin.site.register(SharedRecord)

