"""
Django settings for authors project.

Generated by 'django-admin startproject' using Django 1.11.14.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import dj_database_url
import django_heroku

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET']
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CORS_ORIGIN_ALLOW_ALL = True
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    'corsheaders',
    'django_extensions',
    'rest_framework',
    'rest_framework_swagger',

    'authors.apps.authentication',
    'authors.apps.core',
    'authors.apps.profiles',
    "authors.apps.report",

    'social_django',
    "authors.apps.article",


]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'authors.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.facebook.FacebookAppOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)
# facebook authentication credentials
SOCIAL_AUTH_FACEBOOK_KEY = os.getenv('FB_KEY')
SOCIAL_AUTH_FACEBOOK_SECRET = os.getenv('FB_SECRET')
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    "fields": "id, email, name"
}

# google authentication credentials
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.getenv('GOOGLE_KEY')
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.getenv('GOOGLE_SECRET')

# twitter authentication credentials
SOCIAL_AUTH_TWITTER_KEY = os.getenv('TWITTER_KEY')
SOCIAL_AUTH_TWITTER_SECRET = os.getenv('TWITTER_SECRET')
SOCIAL_AUTH_TWITTER_SCOPE = ['email']

WSGI_APPLICATION = 'authors.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ['DATABASE'],
        'USER': os.environ['USER'],
        'HOST': os.environ['HOST'],
        'PASSWORD': os.environ['PASSWORD']
    }
}

# email send crendetials
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_HOST_USER = os.environ['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']
EMAIL_PORT = os.environ['EMAIL_PORT']
EMAIL_USE_TLS = True
DEFAULT_DOMAIN = os.getenv('DEFAULT_DOMAIN')
# article pagination credentials
PAGE_SIZE = os.environ["PAGE_SIZE"]


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

CORS_ORIGIN_WHITELIST = (
    '0.0.0.0:4000',
    'localhost:4000',
)

# Tell Django about the custom `User` model we created. The string
# `authentication.User` tells Django we are referring to the `User` model in
# the `authentication` module. This module is registered above in a setting
# called `INSTALLED_APPS`.


AUTH_USER_MODEL = 'authentication.User'

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'authors.apps.core.exceptions.core_exception_handler',
    'NON_FIELD_ERRORS_KEY': 'error',

    'DEFAULT_AUTHENTICATION_CLASSES': (
        'authors.apps.authentication.backends.JWTAuthentication',
    ),

}

SWAGGER_SETTINGS = {
    'SHOW_REQUEST_HEADERS': True,
    'USE_SESSION_AUTH': False,
    'DOC_EXPANSION': 'list',
    'SECURITY_DEFINITIONS': {
        'api_key': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    }
}

SITE_ID = 1

django_heroku.settings(locals())
locals()['DATABASES']['default'] = dj_database_url.config(
    default=os.getenv("DATABASE_URL"), ssl_require=not DEBUG)
