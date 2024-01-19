import os
import sys

ENVIRONMENT = os.environ.get('ENV').lower()

if ENVIRONMENT == 'dev':
    from .dev import *
elif ENVIRONMENT == 'prod':
    from .prod import *
else:
    print('!!! Missing ENV variable (dev | prod) !!!')
    sys.exit(1)