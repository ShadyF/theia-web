from django.conf.urls import url
from .views import Editor

urlpatterns = [
    url(r'^$', Editor.as_view(), name='editor'),
    url(r'^sharpen/$', Editor.as_view(), name='processimage')
]
