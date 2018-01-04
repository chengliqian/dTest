"""dTest URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from app1 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', views.login),
    url(r'logout', views.logout),
    url(r'^index', views.index),
    url(r'^add/', views.add),
    url(r'^search_cls/', views.search_cls),
    url(r'^add_cls/', views.add_cls),
    url(r'^edit_cls-(?P<cid>\d+)', views.edit_cls),
    url(r'^delete_cls', views.delete_cls),
    url(r'^search_stu', views.search_stu),
    url(r'^add_stu', views.add_stu),
    url(r'^edit_stu-(?P<sid>\d+)', views.edit_stu),
    url(r'^delete_stu', views.delete_stu),
    url(r'^clas_select/(?P<cousid>\d+)', views.clas_select),
    url(r'^search_course', views.search_course),
    url(r'^del_course', views.del_course),
    url(r'^edit_course',views.edit_course),
    url(r'^add_course',views.add_course),
    url(r'^download_cls',views.download_clas)



]
