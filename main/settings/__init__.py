from decouple import config

ENV = config('ENVIRONMENT', 'production')

ENVIRONMENT = ENV.lower()
if ENVIRONMENT not in ['production', 'dev', 'development']:
    ENVIRONMENT = 'production'


if ENVIRONMENT == 'production':
    from .prod import *

else:
    print("Starting in development mode")
    from .dev import *
