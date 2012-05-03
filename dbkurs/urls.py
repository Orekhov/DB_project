from django.conf.urls import patterns, include, url
from dbkurs import views

urlpatterns = patterns('',
    (r'^$',views.notdelivered),
    (r'^maincss$',views.mcss),
    (r'^customers$',views.customers),
    (r'^outputs$',views.outputs),
    (r'^mainp$',views.mainp),
    (r'^orders$',views.orders),
    (r'^addorder$',views.addorder),
    (r'^thanks$',views.thanks),
    (r'^addcustomer$',views.addcustomer),
    (r'^addoutput$',views.addoutput),
    (r'^customer/(\d{1,3})/$',views.customer),
    (r'^adddelpoint$',views.adddelpoint),
    (r'^delivorder$',views.delivorder),
    (r'^delorderdir$',views.delivorderdirectly),
    (r'^order/(\d{1,3})/$',views.order),
    (r'^othercss$',views.ocss),
    (r'^jquery$',views.jquery),
)
