from django.contrib import admin
from .models import JournalEntry, ShareLink

admin.site.register(JournalEntry)
admin.site.register(ShareLink)