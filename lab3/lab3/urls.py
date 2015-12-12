from django.conf.urls import url, include
from django.contrib import admin
from pheonix.urls import urlpatterns as pheonix_urls

urlpatterns = [
    url(r'', include(pheonix_urls)),
    url(r'^admin/', admin.site.urls),
]
