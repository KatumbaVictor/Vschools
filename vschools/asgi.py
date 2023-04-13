"""
ASGI config for vschools project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
import django

from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from django.conf.urls import url
from decouple import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{config("PROJECT_NAME")}.settings')
django.setup()

from channels.auth import AuthMiddlewareStack
from main.consumers import ChatConsumer, SignalingConsumer
from channels.routing import ProtocolTypeRouter, URLRouter

application = ProtocolTypeRouter({
    'http':get_asgi_application(),
    'websocket':AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    url(r'^MessageSocket/(?P<room_name>[\w.@+-]+)/$', ChatConsumer.as_asgi()),
                    url(r'^signaling-service/(?P<room_name>[\w.@+-]+)/$', SignalingConsumer.as_asgi()),
                ]
            )
        )
    )
})
