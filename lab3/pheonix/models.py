from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class Channel(models.Model):

    class Meta:
        verbose_name = 'channel'
        verbose_name_plural = 'channels'
        default_related_name = 'channels'
        ordering = ['title', ]

    title = models.CharField(max_length=50, null=False, blank=False)
    description = models.CharField(max_length=400, null=True, blank=True)


class Member(User):

    class Meta:
        verbose_name = 'member'
        verbose_name_plural = 'members'
        default_related_name = 'members'
        ordering = ['last_name', 'first_name', ]


class Message(models.Model):

    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'messages'
        default_related_name = 'messages'
        ordering = ['-sent_at', ]

    content = models.TextField(null=False, blank=False)
    sent_at = models.DateTimeField(null=False, auto_now=True)
    sent_by = models.ForeignKey(Member, null=False, on_delete=models.CASCADE)
    channel = models.ForeignKey(Channel, null=True, on_delete=models.SET_NULL)

    def type(self):
        if self.id in Notification.objects.values_list('id', flat=True):
            return Notification.__name__
        elif self.id in Post.objects.values_list('id', flat=True):
            return Post.__name__
        elif self.id in Message.objects.values_list('id', flat=True):
            return Message.__name__

    def instance(self):
        if self.id in Notification.objects.values_list('id', flat=True):
            return Notification.objects.get(id=self.id)
        elif self.id in Post.objects.values_list('id', flat=True):
            return Post.objects.get(id=self.id)
        elif self.id in Message.objects.values_list('id', flat=True):
            return Message.objects.get(id=self.id)


class Notification(Message):

    class Meta:
        verbose_name = 'Notification message'
        verbose_name_plural = 'Notification messages'
        ordering = ['view', 'title', ]

    view_choises = (
        ('info', 'Information'),
        ('alert', 'Alert'),
        ('warning', 'Warning'),
        ('success', 'Success'),
    )

    title = models.CharField(max_length=100, null=False, blank=False)
    view = models.CharField(max_length=8, choices=view_choises, default='info')


class Post(Message):

    class Meta:
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['title', ]

    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=400, null=True, blank=False)
