# Doc found on
# https://exploreflask.com/en/latest/organizing.html#:~:text=Module%20%2D%20A%20module%20is%20a,essentially%20multiple%20modules%20packaged%20together.
# config.py	This file contains most of the configuration variables that your app needs.
DEBUG = False
SQLALCHEMY_ECHO = False  # TODO Delete if not used

CACHE_TYPE = 'SimpleCache'
CACHE_DEFAULT_TIMEOUT = 300

SEND_FILE_MAX_AGE_DEFAULT = 3600
