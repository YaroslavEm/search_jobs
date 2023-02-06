from django.conf.urls.static import static
from django.urls import path

from . import views
from my_site import settings

urlpatterns = [
    path('', views.home_view, name='home'),
    path('list/', views.list_view, name='list'),
    path('global/', views.global_view, name='global'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler400 = views.BadRequest
handler403 = views.AccessForbidden
handler404 = views.pageNotFound
handler500 = views.ServerError