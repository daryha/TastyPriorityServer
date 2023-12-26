
from email_app.views import send_email
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [

    path('email_app/send_email/', send_email, name='send_email'),
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('api/', include('stores.urls')), 
    

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


