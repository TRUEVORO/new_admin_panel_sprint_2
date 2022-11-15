import os

from dotenv import find_dotenv, load_dotenv
from pathlib import Path
from split_settings.tools import include


load_dotenv(find_dotenv('.env.prod'))

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', False) == 'True'

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS').split(' ')

include(
    'components/application.py',
    'components/database.py',
    'components/intern.py',
    'components/pass_valid.py',
    'components/logging.py',
)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Localization
LOCALE_PATHS = ['movies/locale']

# Corsheaders settings
CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:8080',
]
