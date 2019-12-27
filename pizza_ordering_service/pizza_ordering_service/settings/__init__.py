import os

DEBUG = int(os.environ.get("DEBUG", default=0))

if DEBUG:
    from .development import *
else:
    from .production import *
