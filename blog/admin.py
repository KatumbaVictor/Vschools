from django.contrib import admin
from blog.models import *


admin.site.register(BlogCategory)
admin.site.register(Blog)
admin.site.register(BlogComment)
admin.site.register(BlogLike)
