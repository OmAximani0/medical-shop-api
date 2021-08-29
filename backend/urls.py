from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('admin/', admin.site.urls),
    # User Endpoint
    path('user/', include('users.urls')),

    path('store/', include('store.urls')),
    path('medicine/', include('medicine.urls')),
    path('storemedicine/', include('medicine.urls')),
    path('order/', include('order.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)