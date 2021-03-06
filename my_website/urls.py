"""my_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
import get_songlists.views as songListViews

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^GET/avatars/', include('get_songlists.urls')),
    url(r'^songlists/', include('get_songlists.urls')),
    # url(r'^testcookie/', include('get_songlists.urls')),
    url(r'^users/', include('create_account.urls'), name='users'),
    url(r'^comments/', include('django_comments.urls'))
]
