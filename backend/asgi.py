import os
import django
from django.core.asgi import get_asgi_application

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# Configure Django settings before any imports that use models or apps
django.setup()

# Now import the Channels routing and other app-specific modules
from channels.routing import ProtocolTypeRouter, URLRouter
from items.routing import websocket_urlpatterns

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(websocket_urlpatterns),
})
