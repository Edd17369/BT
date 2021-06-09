"""
Django settings for BTsite project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv


# It will load environment variables from a file named .env in the current directory or any of its parents
# load_dotenv does not override existing System environment variables. To override, pass override=True to load_dotenv().
load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# Display of detailed error pages. If your app raises an exception when DEBUG is True, Django will display a detailed traceback,
# including a lot of metadata about your environment, Django will remember every SQL query it executes. This is useful when you’re
# debugging, but it’ll rapidly consume memory on a production server.
DEBUG = False # SECURITY WARNING: don't run with debug turned on in production!


# A list of strings representing the host/domain names that this Django site can serve. This is a security measure to prevent
# HTTP Host header attacks, which are possible even under many seemingly-safe web server configurations.
ALLOWED_HOSTS = ['pezj-djapp.herokuapp.com','127.0.0.1'] # must not be empty in deployment segun py manage.py check --deploy


# Application definition

INSTALLED_APPS = [
    'Btapp', # hay que agregar la aplicacion
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',  # busca los archivos estaticos automaticamente cunado usas runserver when DEBUG = True

    'crispy_forms', # para usar bootstrap en las vistas de los formularios hay que installar el modulo: pip install django-crispy-forms
    'storages', # para django-storages y aws
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    'whitenoise.middleware.WhiteNoiseMiddleware', # Radically simplified static file serving for Python web apps, pip install whitenoise

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'BTsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# Web Server Gateway Interface. A simple calling convention for web servers to forward requests to web applications 
# or frameworks written in the Python programming language.
WSGI_APPLICATION = 'BTsite.wsgi.application'  


# When Gunicorn is installed (pip install gunicorn), a gunicorn command is available which starts the Gunicorn server process. 
# The simplest invocation of gunicorn is to pass the location of a module containing a WSGI application object named application,
# which for a typical Django project would look like: gunicorn myproject.wsgi (Segun django)
# Para deplegar en heroku escribes esto en el Procfile


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

"""DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}"""

""" DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql', # install psycopg2 is required, Psycopg is the most popular PostgreSQL database adapter for Python.
        # estos datos es de cuando creas la base de datos en postgresql
        'NAME': os.getenv('DB_NAME'), # nombre de la db 
        'USER': 'postgres',
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'), 
        'PORT': '5432',
        # If the database backend supports time zones (e.g. PostgreSQL), this option is very rarely needed. It can be changed at any time; the database takes care of converting datetimes to the desired time zone
        #'TIME_ZONE': ''  
    }
} """

DATABASES = {}
import dj_database_url

DATABASES['default'] = dj_database_url.config(conn_max_age=600, ssl_require=True)
# The dj_database_url.config method returns a Django database connection dictionary, populated with all 
# the data specified in your URL. There is also a conn_max_age argument to easily enable Django’s connection pool.

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LOGIN_URL = '/login/' # asociamos el login del sitio al url '/login/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_URL = '/static/' #  this will be used as the base path for asset definitions (theMediaclass) and the staticfiles app.
# Esta diseñado para buscar dentro de la carpeta de la app (Btapp) no del projecto, si lo sacas entonces va a usar STATICFILES_DIRS

# In addition to using a static/ directory inside your apps, you can define a list of directories (STATICFILES_DIRS) 
# in your settings file where Django will also look for static files
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')] 

# In production, you must define a STATIC_ROOT directory where collectstatic will copy them. This is the absolute path to the 
# directory where collectstatic will collect static files for deployment. STATIC_ROOT looks in all locations defined in STATICFILES_DIRS
# and in the 'static' directory of apps specified
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') # segun whitenoise

# Full path to a directory where store uploaded files. These files are not stored in the database, 
# all that will be stored in your database is a path to the file
MEDIA_ROOT = BASE_DIR / Path('static') #os.path.join(BASE_DIR, 'Btapp/static/uploads') 
MEDIA_URL = '/uploads/' # as the base public URL of that directory


# SendGrid
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey' # this is exactly the value 'apikey'
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL') # tiene que ser el correo que diste en sendgrid (no el usuario: os.getenv('DEFAULT_FROM_EMAIL')) 

# Error reporting
SERVER_EMAIL = os.getenv('DEFAULT_FROM_EMAIL') # Default 'root@localhost'. The email address that error messages come from, such as those sent to ADMINS and MANAGERS.
ADMINS = [('Yo', os.getenv('DEFAULT_FROM_EMAIL'))] # who should get details of exceptions raised in the request/response cycle
MANAGERS = [('Yo', os.getenv('DEFAULT_FROM_EMAIL'))] # who should get broken link notifications


# Set this to True to avoid transmitting the CSRF cookie over HTTP accidentally. If this is set to True, the cookie will be
# marked as “secure”, which means browsers may ensure that the cookie is only sent with an HTTPS connection.
#CSRF_COOKIE_SECURE = True # NO tengo un certificado de seguridad SSL para manejar conexiones HTTPS
# If this is set to True, the cookie will be marked as “secure”, which means browsers may ensure that the cookie is only sent 
# under an HTTPS connection.
#SESSION_COOKIE_SECURE = True # NO tengo SSL

# AWS
## django-storages
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage' # To upload your media files to S3 set
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage' # To allow 'collectstatic' to automatically put your static files in your bucket
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_SIGNATURE_VERSION = 's3v4' # used for generating presigned urls. To be able to access your s3 objects in all regions through presigned urls
AWS_S3_REGION_NAME = 'us-east-2' # junto con SIGNATURE_VERSION arregla todos los problemas de css jajajajajaja
AWS_QUERYSTRING_EXPIRE = 86400 # Un dia #The number of seconds that a generated URL is valid for default 3600 1 hora
## bucket S3
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
