from django.conf.urls import url
from backend import views

urlpatterns = [
    url(r'^api/$', views.index, name='index'),
    url(r'^api/owners/$', views.OwnerList.as_view()),
    url(r'^api/owners/(?P<id>[0-9]+)$', views.OwnerDetail.as_view()),
    url(r'^api/events/$', views.EventList.as_view()),
    url(r'^api/events/(?P<id>[0-9]+)$', views.EventDetail.as_view()),
    url(r'^api/cities/$', views.CityList.as_view()),
    url(r'^api/near_events/$', views.NearEventList.as_view()),
    url(r'^api/external_events_handler/$', views.external_events_handler),
]
