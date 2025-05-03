from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.home, name = "home"),
    path('upload/',views.upload_file, name="upload_file" ), 
    path('show_images/', views.show_images, name = "show_images")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
