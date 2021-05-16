"""
Django settings for mainsite project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
from decouple import config, Csv
from datetime import timedelta
import pandas as pd
import pickle

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", cast=bool)

ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())

AUTH_USER_MODEL = "users_app.Users"

SITE_ID = 1

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "import_export",
    "storages",
    "rest_framework",
    "rest_framework.authtoken",
    "management",
    "users_app",
    "products_app",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "mainsite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "mainsite.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# REST API
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # "rest_framework.authentication.BasicAuthentication",
        # "rest_framework.authentication.SessionAuthentication",
        "users_app.auth.TokenAuthentication"
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
}


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "SLIDING_TOKEN_LIFETIME": timedelta(days=1),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]


# aws settings
AWS = config("AWS", cast=bool)
AWS_STATIC_LOCATION = "static"
AWS_PUBLIC_MEDIA_LOCATION = "media/public"
AWS_PRIVATE_MEDIA_LOCATION = "media/private"
AWS_DEFAULT_ACL = "private"

if AWS:
    # aws settings
    AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_REGION_NAME = config("AWS_S3_REGION_NAME")
    AWS_DEFAULT_ACL = config("AWS_DEFAULT_ACL")
    AWS_S3_FILE_OVERWRITE = config("AWS_S3_FILE_OVERWRITE", cast=bool)
    AWS_S3_CUSTOM_DOMAIN = "%s.s3.amazonaws.com" % (
        AWS_STORAGE_BUCKET_NAME
    )  # oneqshop-v1.s3.ap-south-1.amazonaws.com
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    # s3 static settings
    STATICFILES_STORAGE = "mainsite.storage_backends.StaticStorage"
    STATIC_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, AWS_STATIC_LOCATION)
    # s3 public media settings
    DEFAULT_FILE_STORAGE = "mainsite.storage_backends.PublicMediaStorage"
    # s3 private media settings
    AWS_S3_SIGNATURE_VERSION = config("AWS_S3_SIGNATURE_VERSION")
    PRIVATE_FILE_STORAGE = (
        "mainsite.storage_backends.PrivateMediaStorage"
    )  # ?AWSAccessKeyId=AKIAX5GVYLUQZR4HIMXD after url
else:
    STATIC_URL = "/staticfiles/"
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    MEDIA_URL = "/mediafiles/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"


# email
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST")  # mail service smtp
EMAIL_HOST_USER = config("EMAIL_HOST_USER")  # email id
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")  # password
EMAIL_PORT = config("EMAIL_PORT", cast=int)
EMAIL_USE_TLS = config("EMAIL_USE_TLS", cast=bool)

# django-import-export
IMPORT_EXPORT_USE_TRANSACTIONS = True


# PRODUCT_VISUAL_RECOMMEND
with open(
    os.path.join(BASE_DIR, "ai", "product_visual_similarity", "filenames.pickle"), "rb"
) as f:
    PRODUCT_VISUAL_RECOMMEND_IDS = pickle.load(f)
PRODUCT_VISUAL_RECOMMEND_MODEL = pd.read_csv(
    os.path.join(BASE_DIR, "ai", "product_visual_similarity", "model.csv"),
    index_col=[0],
)


# PRODUCT_NAME_RECOMMEND
with open(
    os.path.join(BASE_DIR, "ai", "product_name_similarity", "ids.pickle"), "rb"
) as f:
    PRODUCT_NAME_RECOMMEND_IDS = pickle.load(f)
PRODUCT_NAME_RECOMMEND_MODEL = pd.read_csv(
    os.path.join(BASE_DIR, "ai", "product_name_similarity", "model.csv"), index_col=[0]
)


# USER_BASED_COLLABORATIVE_FILTERING
USER_BASED_COLLABORATIVE_FILTERING_PIVOT_DF = pd.read_csv(
    os.path.join(
        BASE_DIR, "ai", "user_based_collaborative_filtering", "userBased_pivotDF.csv"
    ),
    index_col=[0],
)
USER_BASED_COLLABORATIVE_FILTERING_PREDS_DF = pd.read_csv(
    os.path.join(
        BASE_DIR, "ai", "user_based_collaborative_filtering", "userBased_predsDF.csv"
    ),
    index_col=[0],
)

# ITEM_BASED_COLLABORATIVE_FILTERING
ITEM_BASED_COLLABORATIVE_FILTERING_PIVOT_DF = pd.read_csv(
    os.path.join(
        BASE_DIR, "ai", "item_based_collaborative_filtering", "itemBased_pivotDF.csv"
    ),
    index_col=[0],
)

PRODUCT_VISUAL_RECOMMEND_TOTAL = 3
PRODUCT_NAME_RECOMMEND_TOTAL = 3
USER_BASED_COLLABORATIVE_FILTERING_RECOMMEND_TOTAL = 3
ITEM_BASED_COLLABORATIVE_FILTERING_RECOMMEND_TOTAL = 3
