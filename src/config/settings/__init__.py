from .base import *
from os import getenv


PRODUCTION = int(getenv('PRODUCTION', 0))

if PRODUCTION:
    from .prod import *
else:
    from .dev import *
