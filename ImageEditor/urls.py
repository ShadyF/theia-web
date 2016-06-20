from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Editor.as_view(), name='editor'),
    url(r'^process/$', views.Editor.as_view(), name='processimage'),
    url(r'^filter/(?P<filter_name>\w+)/$', views.apply_color_filter)
]
