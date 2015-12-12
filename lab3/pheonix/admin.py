from django.contrib import admin
from django.contrib.auth.models import Permission
from pheonix.models import Channel, Member, Message, Post, Notification


class MessageAdminView(admin.ModelAdmin):
    list_display = ['sent_by', 'sent_at', ]


class PostAdminView(admin.ModelAdmin):
    list_display = ['title', 'sent_by', 'sent_at']


class NotificationAdminView(admin.ModelAdmin):
    list_display = ['title', 'view', 'sent_by']


class ChannelAdminView(admin.ModelAdmin):

    class MessageInlineView(admin.TabularInline):
        model = Message
        extra = 1

    list_display = ['title', 'description', ]
    inlines = [MessageInlineView, ]


class MemberAdminView(admin.ModelAdmin):

    auth_info_fieldset = (
        'Auth information', {
            'fields': [
                'username',
                'password',
                'last_login'
            ]
        }
    )

    member_info_fieldset = (
        'Member information', {
            'fields': [
                'first_name',
                'last_name',
                'email',
                'date_joined',
            ]
        }
    )

    permissions_fieldset = (
        'Permissons', {
            'fields': [
                'user_permissions',
                'is_staff',
                'is_active',
                'is_superuser',
            ]
        }
    )

    fieldsets = [
        auth_info_fieldset,
        member_info_fieldset,
        permissions_fieldset,
    ]

    list_display = [
        'username',
        'email',
    ]


admin.AdminSite.site_header = 'Pheonix admin site'
admin.AdminSite.site_title = 'Pheonix admin site'
admin.AdminSite.index_title = 'Pheonix'


admin.site.register(Channel, ChannelAdminView)
admin.site.register(Member, MemberAdminView)
admin.site.register(Message, MessageAdminView)
admin.site.register(Post, PostAdminView)
admin.site.register(Notification, NotificationAdminView)
