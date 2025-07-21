from django.conf import settings
from django_hosts import patterns, host

host_patterns = patterns('',
    host(r'www', settings.ROOT_URLCONF, name='www'),
    host(r'forum', 'machina.urls', name='machina'),
    host(f'blog', 'blog.urls', name='blog'),
)