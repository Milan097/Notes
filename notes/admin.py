from django.contrib import admin
from .models import Note, Tag, Share

# Register your models here.
admin.site.register(Tag)
admin.site.register(Note)
admin.site.register(Share)