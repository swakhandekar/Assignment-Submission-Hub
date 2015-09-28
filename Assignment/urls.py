"""Assignment URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from main import views
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$',views.home),
    url(r'^sign_up_stud/',views.sign_up_stud),
    url(r'^sign_up_teach/',views.sign_up_teach),
    url(r'^login/',views.log_in),
    url(r'^create_batches/',views.create_batches),
    url(r'logout/',views.log_out),
    url(r'assignment_view/',views.assignment_view),
    url(r'add_assignment/',views.add_assignment),
    url(r'submit/',views.submit),
    url(r'remark/',views.remark),
    url(r'ret_file/',views.ret_file),
    url(r'check_list',views.check_list),
    url(r'grade_de',views.grade_de),
    url(r'remark_sub',views.remark_sub),
    url(r'contact_us/',views.contact_us)
]
