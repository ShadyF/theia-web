from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Editor.as_view(), name='editor'),
    url(r'^upload/$', views.ImageUploadHandler.as_view(), name='image_upload'),
    url(r'^reset/$', views.reset_image, name='reset_image'),
    url(r'^download/$', views.download_image, name='download_image'),
    url(r'^(?P<operation_type>\w+)/$', views.ImageOperation.as_view(), name='image_operation')
]
