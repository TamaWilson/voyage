from django.conf.urls import url

from . import views

app_name = 'voyage'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^results/$', views.results, name='results'),
    url(r'^insert/$', views.insert, name='insert'),
    url(r'^conectar/$', views.conectar, name='conectar'),

]
