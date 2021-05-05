from django.contrib import admin
from main.models import account_info,posts, saved_posts

admin.site.register(account_info)
admin.site.register(posts)
admin.site.register(saved_posts)