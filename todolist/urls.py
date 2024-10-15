
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from .views import redirect_base
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('',redirect_base),
    path('admin/', admin.site.urls),
    path('',include('tasks.urls')),
    #path('costs/',include('costs.urls')),
    path('costs/', include('costs.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

