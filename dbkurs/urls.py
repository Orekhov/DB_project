from django.conf.urls import patterns, include, url
from dbkurs import views

urlpatterns = patterns('',
    (r'^$',views.mainp),
    (r'^maincss$',views.mcss),
    (r'^customers$',views.customers),
    (r'^outputs$',views.outputs),
    (r'^othercss$',views.ocss),
)
