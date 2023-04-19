import os

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'movies.apps.MoviesConfig',
    'django_extensions',
    'corsheaders',
]

if os.environ.get('DEBUG', 'False').title() == 'True':
    INSTALLED_APPS.append('debug_toolbar')
