from django.contrib import admin
from main.models import account_info, Room, followings, Room_member

admin.site.register(account_info)
admin.site.register(Room_member)
admin.site.register(followings)
admin.site.register(Room)
