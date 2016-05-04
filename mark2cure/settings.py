from celery.schedules import crontab
from datetime import timedelta
import raven

import djcelery
import sys
import os

from configurations import (
    Configuration
)

from configurations.values import (
    Value,
    SecretValue,
    BooleanValue,
    DatabaseURLValue
)


class Base(Configuration):

    djcelery.setup_loader()

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    PROJECT_PATH = os.path.realpath(os.path.join(os.path.dirname(__file__), os.path.pardir))

    @classmethod
    def setup(cls):
        super(Base, cls).setup()

    '''
        cls.RAVEN_CONFIG = {
            'dsn': cls.SENTRY_DSN,
            'release': raven.fetch_git_sha(cls.PROJECT_PATH),
        }
    '''

    SECRET_KEY = SecretValue(environ_prefix='MARK2CURE')
    ADMINS = ()
    MANAGERS = ADMINS
    SITE_ID = 1
    INTERNAL_IPS = ('127.0.0.1',)

    # Application definition
    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        'django_comments',

        'django.contrib.sites',
        'django.contrib.flatpages',
        'django.contrib.webdesign',
        'django.contrib.sitemaps',
        'raven.contrib.django.raven_compat',

        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'allauth.socialaccount.providers.google',

        'djangoratings',
        'djrill',
        'djcelery',
        'robots',
        'corsheaders',

        'grappelli',
        'django.contrib.admin',
        'django_extensions',
        'django_nose',
        'rest_framework',
        'tagging',
        'mptt',
        'brabeion',
        'debug_toolbar',

        # Mark2Cure specific apps
        #'mark2cure.registration',
        'mark2cure.userprofile',
        'mark2cure.team',
        'mark2cure.instructions',
        'mark2cure.training',
        'mark2cure.document',

        'mark2cure.task',
        'mark2cure.task.entity_recognition',
        'mark2cure.task.relation',

        'mark2cure.score',
        'mark2cure.common',
        'mark2cure.talk',
        'mark2cure.api',
        'mark2cure.control',
        'mark2cure.analysis',

        'django.contrib.humanize',
        'widget_tweaks',
        'storages',
        'gunicorn'
    )

    # SENTRY_DSN = SecretValue(environ_prefix='MARK2CURE')
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'root': {
            'level': 'WARNING',
            'handlers': ['sentry'],
        },
        'formatters': {
            'verbose': {
                'format': '%(levelname)s %(asctime)s %(module)s '
                          '%(process)d %(thread)d %(message)s'
            },
        },
        'handlers': {
            'sentry': {
                'level': 'ERROR',
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
                'tags': {'custom-tag': 'x'},
            },
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'formatter': 'verbose'
            }
        },
        'loggers': {
            'django.db.backends': {
                'level': 'ERROR',
                'handlers': ['console'],
                'propagate': False,
            },
            'raven': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
            'sentry.errors': {
                'level': 'DEBUG',
                'handlers': ['console'],
                'propagate': False,
            },
        },
    }

    # AUTHENTICATION_BACKENDS = ('django.contrib.auth.backends.ModelBackend',)
    AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.ModelBackend',

        # `allauth` specific authentication methods, such as login by e-mail
        'allauth.account.auth_backends.AuthenticationBackend',
    )


    MIDDLEWARE_CLASSES = (
        'django.middleware.cache.UpdateCacheMiddleware',

        'django.contrib.sessions.middleware.SessionMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'mark2cure.userprofile.activeuser_middleware.ActiveUserMiddleware',

        'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',

        'django.middleware.cache.FetchFromCacheMiddleware',

        #'account.middleware.LocaleMiddleware',
        #'account.middleware.TimezoneMiddleware',
    )

    ROOT_URLCONF = 'mark2cure.urls'
    WSGI_APPLICATION = 'mark2cure.wsgi.application'

    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.BCryptPasswordHasher',
        'django.contrib.auth.hashers.PBKDF2PasswordHasher',
        'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
        'django.contrib.auth.hashers.SHA1PasswordHasher',
        'django.contrib.auth.hashers.MD5PasswordHasher',
        'django.contrib.auth.hashers.CryptPasswordHasher',
    )

    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'America/Los_Angeles'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    TEMPLATE_LOADERS = (
        ('pyjade.ext.django.Loader', (
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
            'django.template.loaders.eggs.Loader',
        )),
    )

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
        'django.core.context_processors.request',

        'mark2cure.common.context_processors.support_form',
        #'mark2cure.registration.context_processors.inject_signup_forms',
    )

    MEDIA_URL = 'media/'
    MEDIA_ROOT = 'media/'

    STATIC_URL = '/static/'
    STATIC_ROOT = '/static/'

    TEMPLATE_DIRS = (
        PROJECT_PATH + '/templates/',
    )

    STATICFILES_DIRS = (
        PROJECT_PATH + '/static',
        'static'
    )

    FIXTURE_DIRS = (
        PROJECT_PATH + '/fixtures/',
    )

    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    AWS_ACCESS_KEY_ID = SecretValue(environ_prefix='MARK2CURE')
    AWS_SECRET_ACCESS_KEY = SecretValue(environ_prefix='MARK2CURE')
    AWS_STORAGE_BUCKET_NAME = 'mark2cure'

    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        'django.contrib.staticfiles.finders.FileSystemFinder',
    )

    GRAPPELLI_AUTOCOMPLETE_SEARCH_FIELDS = True

    # Admin/Control settings
    ADMIN_PASSWORD = SecretValue(environ_prefix='MARK2CURE')
    ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
    SOUTH_TESTS_MIGRATE = False
    REUSE_DB = 1

    URL_KEYSPACE = os.environ.get('URL_KEYSPACE')
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    # User settings
    AUTH_PROFILE_MODULE = 'userprofile.UserProfile'
    LOGIN_URL = '/registration/login/'
    LOGOUT_URL = '/registration/logout/'
    LOGIN_REDIRECT_URL = '/'

    REST_FRAMEWORK = {
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.BasicAuthentication',
            'rest_framework.authentication.SessionAuthentication',
        )
    }

    ENTREZ_EMAIL = SecretValue(environ_prefix='MARK2CURE')
    ENTREZ_TERMS = ['chordoma', 'breast cancer', 'diabetes']
    ENTREZ_MAX_COUNT = 10

    NCBO_API_KEY = '5dbf6de8-fda5-4ef7-a3a8-bcea293f3715'
    STOP_WORDS = 'protein,gene,disease,disorder,syndrome,chromosome,receptor,cell,\
            orphan,thumb,center,with,involved,image,type,known,encoded,this,both,\
            human,second,near,observed,from,family,width,name,caption,state,\
            structure,MEROPS,Pfam,domain,Symbol,SMART,crystal,analogue,\
            protein family,SCOP,InterPro,EC number,Name,group,related,then,Some,\
            form,http,abstract,content,liter,levels,enzyme,drugs,into,slow,\
            intermediate,bound,Citation,when,down,After'

    POSTIVE_FLATTER = ['Bravo', 'Wow', 'Super', 'Terrific', 'Cool', 'Amazing', 'Superb', 'Brilliant', 'Fantastic', 'Fabulous', 'You\'re a Champion', 'Well done', 'You rock', 'Great job', 'Tip top', 'Good thinking', 'Keep it up', 'Way to go', 'Right on', 'Top stuff', 'Take a bow', 'Unreal', 'Impressed', 'Great stuff', 'Awesome', 'Nice going', 'Very Creative', 'Thank You', 'Beautiful', 'Very proud', 'Good for you', 'Give me five', 'You make me happy', 'A+', 'A++', 'AA+', 'Fab', 'Rad', 'A+++', 'AAA+', 'A-OK', 'Best', 'Cool', 'Deal', 'Fast', 'Fine', 'Item', 'Nice', 'Safe', 'Thx!', 'WOW!', 'Prime', 'Solid', 'Super', 'Sweet', 'Thanx', 'Whoa!', 'Groovy', 'Honest', 'Speedy', 'Superb', 'Sweeet', 'Thanks', 'Zowie!', 'Amazing', 'Awesome', 'Quality', 'Service', 'Sweeeet', 'Glorious', 'Stunning', 'Superior', 'The Best', 'The Bomb', 'Thrilled', 'Way Cool', 'Brilliant', 'Competent', 'Delighted', 'Excellent', 'Exquisite', 'Marvelous', 'Overjoyed', 'Satisfied', 'Thank You', 'Top Notch', 'Unrivaled', 'Wonderful', 'A Home Run', 'Astounding', 'Delightful', 'Impressive', 'Incredible', 'Super Cool', 'Super Fast', 'Supersonic', 'Astonishing', 'Fascinating', 'Interesting', 'Magnificent', 'No Problems', 'Outstanding', 'Splendorous', 'Trustworthy', 'Unsurpassed', 'Wicked Cool', 'Breathtaking', 'Looking Good', 'Overwhelming!', 'Unbelievable!', 'Awe Inspiring', 'Lickety Split', 'Splendiferous', 'Thanks A Ton!', 'Extremely Cool', 'Satisfied 100%', 'Extremely Happy', 'Great Condition', 'Above And Beyond', 'State Of The Art', 'Thanks A Million!', 'Unbelievably Cool', 'Expertly Described', 'Extremely Satisfied', 'Great Communication', 'Greatly Appreciated', 'Beyond My Wildest Dreams', 'Supercalifragilisticexpialidocious', 'Thank You! Thank You! Thank You!']
    SUPPORT_FLATTER = ['You can do it', 'Nice Try', 'Don\'t give up', 'Every bit counts', 'Thank you', 'Keep going', 'You can do better than that']

    # User is online if they've been last seen 5min ago
    USER_ONLINE_TIMEOUT = 300


    BROKER_URL = SecretValue(environ_prefix='MARK2CURE')
    CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
    CELERY_TIMEZONE = 'America/Los_Angeles'
    CELERYBEAT_SCHEDULE = {
        'check-system-uptime': {
            'task': 'mark2cure.common.tasks.check_system_uptime',
            'schedule': timedelta(seconds=30)
        },
        'check-corpus': {
            'task': 'mark2cure.document.tasks.check_corpus_health',
            'schedule': timedelta(minutes=10)
        },
        'group-analysis': {
            'task': 'mark2cure.analysis.tasks.group_analysis',
            'schedule': crontab(hour=1, minute=30)
        },
    }

    LOGIN_URL = 'account_login'
    # LOGOUT_URL = '/registration/logout/'
    # LOGIN_REDIRECT_URL = '/'
    ROBOTS_USE_SITEMAP = True

    # Email settings management
    DEFAULT_FROM_EMAIL = 'Mark2Cure <contact@mark2cure.org>'
    SERVER_EMAIL = DEFAULT_FROM_EMAIL
    MANDRILL_API_KEY = SecretValue(environ_prefix='MARK2CURE')
    EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"

    # User account management
    ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = ' (TODO) '
    ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 30
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_SIGNUP_PASSWORD_VERIFICATION = True
    ACCOUNT_UNIQUE_EMAIL = True
    ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
    ACCOUNT_USERNAME_MIN_LENGTH = 5
    ACCOUNT_USERNAME_BLACKLIST = ['admin', 'owner', 'user']
    ACCOUNT_USERNAME_REQUIRED = True
    ACCOUNT_PASSWORD_MIN_LENGTH = 6
    ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
    ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
    ACCOUNT_SESSION_REMEMBER = True
    ACCOUNT_TEMPLATE_EXTENSION = 'jade'
    SOCIALACCOUNT_QUERY_EMAIL = ACCOUNT_EMAIL_REQUIRED
    SOCIALACCOUNT_PROVIDERS = { 'google': {
                                    'SCOPE': ['profile', 'email'],
                                    'AUTH_PARAMS': { 'access_type': 'online' }
                              }}


class Development(Base):
    LOCAL = True
    DEBUG = True
    TEMPLATE_DEBUG = True

    CORS_ORIGIN_ALLOW_ALL = True
    ALLOWED_HOSTS = ['*']

    DATABASES = DatabaseURLValue(environ_prefix='MARK2CURE')

    if 'test' in sys.argv:
        import dj_database_url
        DATABASES = {'default': dj_database_url.parse('sqlite://' + Base.PROJECT_PATH + '/test_db.sqlite')}
        SOUTH_TESTS_MIGRATE = True

        SOUTH_LOGGING_ON = True
        SOUTH_LOGGING_FILE = Base.PROJECT_PATH + '/south_logging_file'


    DOMAIN = 'localhost:8000'
    DEBUG_FILENAME = 'mark2cure-local-debug.log'
    VERSION = '0.1 (Local)'

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }


class Production(Base):
    LOCAL = False
    DEBUG = False
    TEMPLATE_DEBUG = False

    CORS_ORIGIN_ALLOW_ALL = False
    ALLOWED_HOSTS = ['.mark2cure.org']

    DATABASES = DatabaseURLValue(environ_prefix='MARK2CURE')

    DOMAIN = 'mark2cure.org'
    DEBUG_FILENAME = 'mark2cure-debug.log'
    VERSION = '0.1 (Production)'

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211',
        }
    }

    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'

    # SESSION_COOKIE_SECURE = True
    # CSRF_COOKIE_SECURE = True
