from django.conf.urls import url, include
from pheonix.views import (
    LoginView,
    RegistrationView,
    ChannelsView,
    MessagesView,
    HomeView,
)


urlpatterns = [
    url(r'^channels/(?P<channel_title>\D+)/?$', MessagesView.as_view(), name="messages_view"),
    url(r'^channels/?$', ChannelsView.as_view(), name='channels_view'),
    url(r'^in/?$', LoginView.as_view(), name='login_view'),
    url(r'^up/?$', RegistrationView.as_view(), name='registration_view'),
    url(r'^$', HomeView.as_view(), name='home_view'),
]
