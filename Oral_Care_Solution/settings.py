from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-ujzp4l^y3ou@%sd+%s$g#+=p@_l5-bl)d%t4q6rk=qd@_u&sx8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'OCS_APP',
    'userauths',
    'taggit',
    'ckeditor',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Oral_Care_Solution.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'OCS_APP.context_processor.default',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Oral_Care_Solution.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_SETTINGS = {
    'site_title': 'Oral Care Solution Admin',
    'site_header':'Oral Care Solution',
    'site_brand':'OCS',
    'site_logo':'assets/imgs/theme/OCS.png',
    'welcome_sign':'ADMIN PANEL',
    'site_logo_classes':'img-square',
    "copyright":"OCS Ltd",
    #"search_model":["OCS_APP.Order", "OCS_APP.Product"],
    "topmenu_links":[{"name":"Home", "url":"http://127.0.0.1:8000/"}, {"name": "Shop",  "url":"http://127.0.0.1:8000/shop/"}],
    "hide_apps":['Taggit', 'auth'],
    "order_with_respect_to":['userauths', 'OCS_APP', 'OCS_APP.Category', 'OCS_APP.Manufacturer', 'OCS_APP.Product', 'OCS_APP.CartOrder', 'OCS_APP.CartOrderItems', 'OCS_APP.ProductReview'],
    "icons":{"OCS_APP.Category":"fas fa-list", "OCS_APP.CartOrder":"fas fa-box", "OCS_APP.CartOrderItems":"fas fa-boxes", "OCS_APP.ProductReview":"fas fa-search", "OCS_APP.Manufacturer":"fas fa-industry", "OCS_APP.Product":"fas fa-tooth", "OCS_APP.Address":"fas fa-map-marker-alt", "userauths.User":"fas fa-user", "userauths.Profile":"fas fa-id-card"},
    #"show_ui_builder": True,
}

JAZZMIN_UI_TWEAKS = {
    "theme":"flatly",
    "dark_mode_theme":"darkly",
}

LOGIN_URL = 'userauths:log-in'

PAYPAL_RECEIVER_EMAIL = 'businessdestiny@gmail.com'
PAYPAL_TEST = True

AUTH_USER_MODEL = 'userauths.User'

CKEDITOR_UPLOAD_PATH = 'uploads/'

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_AGE = 86400

CKEDITOR_CONFIGS = {
    'default': {
        'skin':'moono',
        'codeSnippet_theme':'monokai',
        'toolbar':'all',
        'extraPlugins':','.join(
            [
                'codesnippet',
                'widget',
                'dialog',
            ]
        ),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'aliahmedchamp@gmail.com'
EMAIL_HOST_PASSWORD = 'vkyq zgbn jpse wczd'