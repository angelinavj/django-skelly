from django.conf.urls.defaults import *
from myapp.views import OrderView, OrderListView

urlpatterns = patterns('myapp.views',
  url(r'^$', 'index', name='home'),
  url(r'^contact/$', 'contact', name='myapp_contact'),
  url(r'^payment/$', 'payment', name='myapp_payment'),

  url(r'^order/(?P<pk>\d+)/$', OrderView.as_view(), name='order_detail'),
  url(r'^orders/$', OrderListView.as_view(), name='order_list'),
)
