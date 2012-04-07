from django.conf.urls import patterns, include, url
from dbkurs import views

urlpatterns = patterns('',
    (r'^$',views.mainp),
    (r'^maincss$',views.mcss),
    (r'^clients$',views.clients),
    (r'^othercss$',views.ocss),
)
