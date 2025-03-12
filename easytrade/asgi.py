import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'easytrade.settings')
<<<<<<< HEAD

=======
>>>>>>> 1f1ec4b928cddfc092349168b2cf9870c33751a0
application = get_asgi_application()
