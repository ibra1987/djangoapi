from django.urls import path
from . import controllers
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('remove-background', controllers.remove_background,
         name="remove_background"),
    path('compress-image', controllers.compress_image,
         name="compress_image"),
    path('convert-image', controllers.convert_image,
         name="convert_image"),
]

urlpatterns += staticfiles_urlpatterns()
