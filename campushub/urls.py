from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from students import views as student_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('students/', include('students.urls')),
    path('dashboard/', student_views.dashboard, name='dashboard'),
    path('', student_views.landing, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
