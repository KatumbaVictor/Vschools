from django.contrib import admin
from main.models import account_info, Room, Room_member, scheduledmeeting
from passkeys.models import UserPasskey

admin.site.register(account_info)
admin.site.register(Room_member)
admin.site.register(Room)
admin.site.register(scheduledmeeting)
admin.site.register(UserPasskey)