from django.contrib import admin

from .models import ChatRoom, WSAuth, ActiveChannel


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    pass


@admin.register(WSAuth)
class WSAuthAdmin(admin.ModelAdmin):
    pass


@admin.register(ActiveChannel)
class ActiveChannelAdmin(admin.ModelAdmin):
    pass
