from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView

from pheonix.models import Member, Channel, Message, Notification, Post
from pheonix.forms import (
    LoginForm,
    RegistrationForm,
    AddChannelForm,
    MessageForm,
    NotificationForm,
    PostForm
)


class HomeView(TemplateView):
    
    template_name = 'pheonix/main.html'


class LoginView(TemplateView):

    template_name = 'pheonix/login.html'

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        context['login_form'] = LoginForm()
        response = render(request, self.template_name, context=context)
        return response

    def post(self, request, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return redirect('channels_view')
            else:
                if User.objects.filter(username=username).exists():
                    form.add_error('password', 'Wrong password')
                else:
                    form.add_error('username', 'Unknown user')

        context = self.get_context_data(**kwargs)
        context['login_form'] = form
        return render(request, self.template_name, context=context)


class RegistrationView(TemplateView):

    template_name = 'pheonix/registation.html'

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        context['registration_form'] = RegistrationForm()
        return render(request, self.template_name, context=context)

    def post(self, request, **kwargs):
        form  = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            if not User.objects.filter(username=username).exists():
                Member.objects.create_user(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password'],
                    email=form.cleaned_data['email'],
                    first_name=form.cleaned_data['first_name'],
                    last_name=form.cleaned_data['last_name'],
                )
                return redirect('login_view')
            else:
                form.add_error('username', 'Already exists')

        context = self.get_context_data(**kwargs)
        context['registration_form'] = form
        return render(request, self.template_name, context=context)


class ChannelsView(LoginRequiredMixin, TemplateView):

    login_url = 'login_view'
    template_name = 'pheonix/channels.html'

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        context['channels'] = Channel.objects.all()
        context['add_channel_form'] = AddChannelForm
        return render(request, self.template_name, context=context)

    def post(self, request, channel=None, **kwargs):
        form = AddChannelForm(request.POST)
        if form.is_valid():
            form.save()
            return self.get(request, **kwargs)
        else:
            context = self.get_context_data(**kwargs)
            context['add_channel_form'] = form
            context['channels'] = Channel.objects.all()
            context['some_erors'] = 'in'
            return render(request, self.template_name, context=context)

class MessagesView(LoginRequiredMixin, TemplateView):

    login_url = 'login_view'
    template_name = 'pheonix/messages.html'

    def get_context_data(self, request, channel_title, **kwargs):
        context = super(MessagesView, self).get_context_data(**kwargs)
        channel = get_object_or_404(Channel.objects, title=channel_title)
        context['channel'] = channel
        context['send_message_form'] = MessageForm()
        context['send_notification_form'] = NotificationForm()
        context['create_post_form'] = PostForm()
        return context
        context = self.get_context_data(request, channel_title, **kwargs)

    def get(self, request, channel_title=None, **kwargs):
        context = self.get_context_data(request, channel_title, **kwargs)
        return render(request, self.template_name, context=context)


    def post(self, request, channel_title=None, **kwargs):
        current_member = Member.objects.get(username=request.user.username)
        current_channel = Channel.objects.get(title=channel_title)
        form_type = request.POST.get('form_type', None)

        if form_type == 'send_message':
            form = MessageForm(request.POST)
            if form.is_valid():
                print User.objects.get(username=request.user.username)
                Message.objects.create(
                    content=form.cleaned_data['content'],
                    sent_by=current_member,
                    channel=current_channel,
                )
                return self.get(request, channel_title, **kwargs)
            else:
                context = self.get_context_data(request, channel_title, **kwargs)
                context['send_message_form'] = form
                context['message_form_collapsed'] = 'in'
                return render(request, self.template_name, context=context)

        elif form_type == 'send_notification':
            form = NotificationForm(request.POST)
            if form.is_valid():
                Notification.objects.create(
                    title=form.cleaned_data['title'],
                    content=form.cleaned_data['content'],
                    view=form.cleaned_data['view'],
                    sent_by=current_member,
                    channel=current_channel,
                )
                return self.get(request, channel_title, **kwargs)
            else:
                context = self.get_context_data(request, channel_title, **kwargs)
                context['send_notification_form'] = form
                context['notification_form_collapsed'] = 'in'
                return render(request, self.template_name, context=context)

        elif form_type == 'create_post':
            form = PostForm(request.POST)
            if form.is_valid():
                Post.objects.create(
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    content=form.cleaned_data['content'],
                    sent_by=current_member,
                    channel=current_channel,
                )
                return self.get(request, channel_title, **kwargs)
            else:
                context = self.get_context_data(request, channel_title, **kwargs)
                context['create_post_form'] = form
                context['post_form_collapsed'] = 'in'
                return render(request, self.template_name, context=context)
