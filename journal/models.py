from django.db import models
from django.contrib.auth.models import User
import uuid

class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    text = models.TextField(blank=True)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    audio = models.FileField(upload_to='audio/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    location = models.CharField(max_length=255, blank=True)  # e.g., "New York"
    sentiment_score = models.FloatField(null=True, blank=True)  # NLTK result
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"

class ShareLink(models.Model):
    entry = models.ForeignKey(JournalEntry, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Share {self.entry.id} - {self.token}"