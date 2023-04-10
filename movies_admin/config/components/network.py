import os

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

if os.environ.get('DEBUG', 'False').title() == 'True':
    MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware', *MIDDLEWARE]

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'

INTERNAL_IPS = [
    "127.0.0.1",
]

CORS_ORIGIN_ALLOW_ALL = os.environ.get('DEBUG', 'False').title() == 'True'
