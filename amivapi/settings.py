# -*- coding: utf-8 -*-
#
# license: AGPLv3, see LICENSE for details. In addition we strongly encourage
#          you to buy us beer if we meet and you like the software.

"""Default settings for all environments.

These settings will be extended by additional config files in ROOT/config.
Run `python manage.py create_config` to create such a config file.
"""

from os.path import abspath, dirname, join
from datetime import timedelta

# Custom
ROOT_DIR = abspath(join(dirname(__file__), ".."))

# Flask
DEBUG = False
TESTING = False

# Flask-SQLALchemy

# Eve
ID_FIELD = "id"
AUTH_FIELD = "_author"
DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
BANDWIDTH_SAVER = False
RESOURCE_METHODS = ['GET', 'POST']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']
PUBLIC_METHODS = ['GET']  # This is the only way to make / public
XML = False

# Eve, file storage options
RETURN_MEDIA_AS_BASE64_STRING = False
EXTENDED_MEDIA_INFO = ['filename', 'size', 'content_url']

# Custom Default language
DEFAULT_LANGUAGE = 'de'
SESSION_TIMEOUT = timedelta(days=365)

# Text for automatically sent mails

# First argument is role name
PERMISSION_EXPIRED_WARNMAIL_SUBJECT = (
    "Your permissions as %(role)s at AMIV are about to expire")
# First argument is name, second role, third admin email
PERMISSION_EXPIRED_WARNMAIL_TEXT = (
    "Hello %(name)s,\nYour permissions as %(role)s at AMIV will expire in 14 "
    "days. If you want to get them renewed please sent an E-Mail to "
    " %(admin_mail)s.\n\nRegards\n\nAutomatically sent by AMIV API"
)

# This is a list of which groups exist to grant permissions. It should be
# possible to change anything without breaking stuff.
ROLES = {
    'vorstand': {
        'users': {
            'GET': 1,
            'POST': 1,
            'PATCH': 1,
            'PUT': 1,
            'DELETE': 1,
        },
        'permissions': {
            'GET': 1,
            'POST': 1,
            'PATCH': 1,
            'PUT': 1,
            'DELETE': 1
        },
        'groups': {
            'GET': 1,
            'POST': 1,
            'PATCH': 1,
            'PUT': 1,
            'DELETE': 1
        },
        'forwardaddresses': {
            'GET': 1,
            'POST': 1,
            'PATCH': 1,
            'PUT': 1,
            'DELETE': 1
        },
        'groupusermembers': {
            'GET': 1,
            'POST': 1,
            'PATCH': 1,
            'PUT': 1,
            'DELETE': 1
        },
        'groupaddressmembers': {
            'GET': 1,
            'POST': 1,
            'PATCH': 1,
            'PUT': 1,
            'DELETE': 1
        },
        'sessions': {
            'GET': 1,
            'DELETE': 1
        },
        'events': {
            'GET': 1,
            'POST': 1,
            'PATCH': 1,
            'PUT': 1,
            'DELETE': 1
        },
        'eventsignups': {
            'GET': 1,
            'POST': 1,
            'PATCH': 1,
            'PUT': 1,
            'DELETE': 1
        },
        'files': {
            'GET': 1,
            'POST': 1,
            'PATCH': 1,
            'PUT': 1,
            'DELETE': 1
        },
        'studydocuments': {
            'GET': 1,
            'POST': 1,
            'PATCH': 1,
            'PUT': 1,
            'DELETE': 1
        },
        'joboffers': {
            'GET': 1,
            'POST': 1,
            'PATCH': 1,
            'PUT': 1,
            'DELETE': 1
        }
    },
    'read-everything': {
        'users': {
            'GET': 1,
        },
        'permissions': {
            'GET': 1,
        },
        'groups': {
            'GET': 1,
        },
        'forwardaddresses': {
            'GET': 1,
        },
        'groupusermembers': {
            'GET': 1,
        },
        'groupaddressmembers': {
            'GET': 1,
        },
        'sessions': {
            'GET': 1,
        },
        'events': {
            'GET': 1,
        },
        'eventsignups': {
            'GET': 1,
        },
        'files': {
            'GET': 1,
        },
        'studydocuments': {
            'GET': 1,
        },
        'joboffers': {
            'GET': 1,
        }
    },
    'event-admin': {
        'events': {
            'GET': 1,
            'POST': 1,
            'PATCH': 1,
            'PUT': 1,
            'DELETE': 1
        },
        'eventsignups': {
            'GET': 1,
            'POST': 1,
            'PATCH': 1,
            'PUT': 1,
            'DELETE': 1
        }
    },
    'job-admin': {
        'files': {
            'GET': 1,
            'POST': 1,
            'PATCH': 1,
            'PUT': 1,
            'DELETE': 1
        },
        'joboffers': {
            'GET': 1,
            'POST': 1,
            'PATCH': 1,
            'PUT': 1,
            'DELETE': 1
        }
    },
    'mail-admin': {
        'groups': {
            'GET': 1,
            'POST': 1,
            'PATCH': 1,
            'PUT': 1,
            'DELETE': 1
        },
        'forwardaddresses': {
            'GET': 1,
            'POST': 1,
            'PATCH': 1,
            'PUT': 1,
            'DELETE': 1
        },
        'groupusermembers': {
            'GET': 1,
            'POST': 1,
            'PATCH': 1,
            'PUT': 1,
            'DELETE': 1
        },
        'groupaddressmembers': {
            'GET': 1,
            'POST': 1,
            'PATCH': 1,
            'PUT': 1,
            'DELETE': 1
        }
    },
    'studydocs-admin': {
        'files': {
            'GET': 1,
            'POST': 1,
            'PATCH': 1,
            'PUT': 1,
            'DELETE': 1
        },
        'studydocuments': {
            'GET': 1,
            'POST': 1,
            'PATCH': 1,
            'PUT': 1,
            'DELETE': 1
        }
    }
}
