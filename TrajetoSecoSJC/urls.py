"""tg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.contrib.auth import urls as registration
from django.views.generic import TemplateView

admin.autodiscover()

urlpatterns = [

    url(r'^$', TemplateView.as_view(template_name='index.html')),

    url(r'^accounts/', include(registration)),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^dados/', include('TrajetoSecoSJC.dados.urls')),
    url(r'^geo/', include('TrajetoSecoSJC.geo.urls')),

    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),

]
