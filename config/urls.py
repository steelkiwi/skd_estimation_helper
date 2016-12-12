"""est URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from apps.core import views as core_views

urlpatterns = [
    url(r'^admin/estimation-table/(?P<pk>\d+)/', core_views.EstimationDetailView.as_view(), name='estimation-table'),
    url(r'^admin/employee-rates-count/(?P<pk>\d+)', core_views.EmployeeRateCountUpdateView.as_view(), name='employee-rate-count-update'),
    url(r'^admin/', admin.site.urls),
]
