from django.conf.urls import patterns, include, url
from dbkurs import views

urlpatterns = patterns('',
    (r'^$',views.mainp),
    (r'^maincss$',views.mcss),
    (r'^customers$',views.customers),
    (r'^outputs$',views.outputs),
    (r'^notdelivered$',views.notdelivered),
    (r'^orders$',views.orders),
    (r'^addorder$',views.addorder),
    (r'^thanks$',views.thanks),
    (r'^addcustomer$',views.addcustomer),
    (r'^addoutput$',views.addoutput),
    (r'^othercss$',views.ocss),
)
