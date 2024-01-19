import dj_database_url
from dotenv import load_dotenv
from .base import *

load_dotenv(os.path.join(BASE_DIR, '.env.dev'))

SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
DEBUG = os.environ.get('DJANGO_DEBUG', default='False')

CSRF_TRUSTED_ORIGINS = os.environ.get('DJANGO_ALLOWED_ORIGINS').split(' ')
ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS').split(' ')
CORS_ORIGIN_WHITELIST = os.environ.get('DJANGO_ALLOWED_ORIGINS').split(' ')

DATABASE_URL = os.getenv('DATABASE_URL')

DATABASES = {
    'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=1800),
}