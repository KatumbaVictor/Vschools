"""
ASGI config for vschools project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os


from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from django.conf.urls import url
from main.consumers import ChatConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vschools.settings')

application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket':AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    url(r'^meet/(?P<room_name>[\w.@+-]+)/(?P<uid>[\w.@+-]+)/(?P<role>[\w.@+-]+)/$', ChatConsumer.as_asgi())
                ]
            )
        )
    )
})
