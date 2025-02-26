# TimeLens - A Personal Time Travel Journal

TimeLens is a web application built with Django, HTML, and plain CSS, using SQLite3 as the database. Users can document their life moments with text, photos, audio, and video, view them on a timeline, analyze sentiment, and share entries privately.

## Features
- **Timeline**: View all journal entries chronologically.
- **Entry Creation**: Add moments with text, media, and location.
- **Sharing**: Generate expiring links to share entries.
- **Insights**: Basic stats like total entries and average sentiment.
- **Custom CSS**: Futuristic design without external frameworks.

## Tech Stack
- **Backend**: Django (Python)
- **Frontend**: HTML, Plain CSS
- **Database**: SQLite3
- **Media Processing**: FFmpeg (`ffmpeg-python`), Pillow
- **Sentiment Analysis**: NLTK

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/stive1213/timelens.git
   cd timelens
2.Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3.Install dependencies:
pip install django ffmpeg-python pillow nltk

4.Install FFmpeg on your system (e.g., brew install ffmpeg on macOS, apt-get install ffmpeg on Ubuntu).

5.Run migrations and create a superuser:
python manage.py migrate
python manage.py createsuperuser

6.Start the development server:
python manage.py runserver

7.Visit http://127.0.0.1:8000/ and log in.

Usage
Log in to create and view your timeline.
Add entries with media to test FFmpeg/Pillow processing.
Share entries and check the insights page for stats.