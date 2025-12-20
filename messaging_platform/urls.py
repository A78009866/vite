from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from vite import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.splash, name='splash'), # الصفحة الترحيبية
    path('home/', views.home, name='home'),
    path('register/', views.register, name='register'), # رابط التسجيل
    path('accounts/login/', auth_views.LoginView.as_view(template_name='social/login.html'), name='login'),
    path('vite/', include('vite.urls')), # تأكد أن ملف vite/urls.py يحتوي على المسارات الداخلية
]
