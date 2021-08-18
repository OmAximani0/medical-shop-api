from django.contrib import admin

from .models import Medicine, StoreMedicine

admin.site.register(Medicine)
admin.site.register(StoreMedicine)