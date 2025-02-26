from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import JournalEntry, ShareLink
from .forms import JournalEntryForm
from datetime import datetime, timedelta
import ffmpeg
from PIL import Image
import os
from django.conf import settings
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from django.db import models

# Download NLTK data (run once)
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

@login_required
def timeline(request):
    entries = JournalEntry.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'journal/timeline.html', {'entries': entries})

@login_required
def create_entry(request):
    if request.method == 'POST':
        form = JournalEntryForm(request.POST, request.FILES)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.timestamp = form.cleaned_data['timestamp']

            # Save the entry to the database first to ensure files are written to disk
            entry.save()

            # Process media files after saving
            if entry.photo:
                img = Image.open(entry.photo.path)
                img.thumbnail((300, 300))  # Resize to max 300x300
                img.save(entry.photo.path)
            if entry.audio:
                audio_path = entry.audio.path
                output_path = audio_path.replace('.wav', '_converted.mp3')  # Example conversion
                try:
                    stream = ffmpeg.input(audio_path)
                    stream = ffmpeg.output(stream, output_path, format='mp3')
                    ffmpeg.run(stream)
                    os.remove(audio_path)
                    entry.audio.name = entry.audio.name.replace('.wav', '_converted.mp3')
                    entry.save()  # Update the entry with the new file name
                except ffmpeg.Error as e:
                    print(f"FFmpeg error: {e}")
            if entry.video:
                video_path = entry.video.path
                output_path = video_path.replace('.mov', '_converted.mp4')  # Example conversion
                try:
                    stream = ffmpeg.input(video_path)
                    stream = ffmpeg.output(stream, output_path, vcodec='libx264')
                    ffmpeg.run(stream)
                    os.remove(video_path)
                    entry.video.name = entry.video.name.replace('.mov', '_converted.mp4')
                    entry.save()  # Update the entry with the new file name
                except ffmpeg.Error as e:
                    print(f"FFmpeg error: {e}")

            # Sentiment analysis
            if entry.text:
                sentiment = sia.polarity_scores(entry.text)
                entry.sentiment_score = sentiment['compound']
                entry.save()  # Save sentiment score

            return redirect('timeline')
    else:
        form = JournalEntryForm()
    return render(request, 'journal/create_entry.html', {'form': form})

@login_required
def share_entry(request, entry_id):
    entry = get_object_or_404(JournalEntry, id=entry_id, user=request.user)
    share_link = ShareLink.objects.create(
        entry=entry,
        expires_at=datetime.now() + timedelta(days=7)
    )
    share_url = request.build_absolute_uri(f'/shared/{share_link.token}/')
    return render(request, 'journal/share_entry.html', {'share_url': share_url})

def view_shared_entry(request, token):
    share_link = get_object_or_404(ShareLink, token=token)
    if share_link.expires_at < datetime.now():
        return HttpResponseForbidden("This link has expired.")
    return render(request, 'journal/view_shared.html', {'entry': share_link.entry})

@login_required
def insights(request):
    entries = JournalEntry.objects.filter(user=request.user)
    total_entries = entries.count()
    avg_sentiment = entries.aggregate(models.Avg('sentiment_score'))['sentiment_score__avg'] or 0
    return render(request, 'journal/insights.html', {
        'total_entries': total_entries,
        'avg_sentiment': avg_sentiment
    })