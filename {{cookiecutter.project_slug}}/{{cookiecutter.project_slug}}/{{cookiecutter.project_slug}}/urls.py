"""music_bucks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from common import views as common_views


urlpatterns = [
    path('', common_views.index),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path("register/", common_views.register, name="register"),
    re_path(r'^activate/(?P<activation_key>[-:\w]+)/$',
            common_views.activate_user_account,
            name='activate_user_account'),
]
handler403 = 'common.views.permission_error_403'
handler404 = 'common.views.page_not_found_404'
handler500 = 'common.views.page_error_500'
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
