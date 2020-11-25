from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from neparu import views

urlpatterns = [
    path('',include('neparu.urls')),
    path('admin/', admin.site.urls),
    path('neparu/', include('neparu.urls')),
    path('auth/password_change/done /',include('neparu.urls')),
    path('social-auth/', include('social_django.urls', namespace="social")),
    path('auth/', include('django.contrib.auth.urls')),
 ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

