from django import forms
from django.core.validators import EmailValidator
from pheonix.models import Member, Channel, Message, Notification, Post


class LoginForm(forms.Form):

    username = forms.CharField(
        max_length=100, required=True, help_text='Username',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Username',
            }
        )
    )

    password = forms.CharField(
        max_length=100, required=True, help_text='Password',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Password',
                'type': 'password',
            }
        )
    )


class RegistrationForm(forms.ModelForm):

    class Meta:
        model = Member
        fields = [
            'username',
            'password',
            'email',
            'first_name',
            'last_name'
        ]
        help_texts = {
            'username': 'Username',
            'password': 'Password',
            'email': 'Your email',
            'first_name': 'Your first name',
            'last_name': 'Your last name',
        }
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Username',
                }
            ),
            'password': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Password'
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Email',
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'First name',
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Last name',
                }
            )
        }


class AddChannelForm(forms.ModelForm):

    class Meta:
        model = Channel
        fields = (
            'title',
            'description'
        )
        help_texts = {
            'title': 'Title of a new channel',
            'description': 'Description of a new channel (optional)'
        }
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Title',
                }
            ),
            'description': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Description',
                }
            )
        }


class MessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = (
            'content',
        )
        help_texts = {
            'content': 'Text of your message'
        }
        widgets = {
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Message',
                    'rows': 3,
                }
            )
        }


class NotificationForm(forms.ModelForm):

    class Meta:
        model = Notification
        fields = (
            'title',
            'content',
            'view'
        )
        help_texts = {
            'title': 'Title of your notification',
            'content': 'Text of your notification',
            'view': 'Type of your notification',
        }
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Title',
                }
            ),
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Text',
                    'rows': 3,
                }
            ),
            'view': forms.Select(
                choices=Notification.view_choises,
                attrs={
                    'class': "selectpicker",
                }
            )
        }


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = (
            'title',
            'description',
            'content'
        )
        help_texts = {
            'title': 'Title of your post',
            'description': 'Description of your post',
            'content': 'Text of your post',
        }
        widgets = {
            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Title',
                }
            ),
            'description': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Description',
                }
            ),
            'content': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Text',
                    'rows': 3,
                }
            )
        }
