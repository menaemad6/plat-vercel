"""social_book URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
]

urlpatterns += [
    path('admin/', admin.site.urls),
    path('', include('main.functions-urls')),
    path('', include('student.functions-urls')),
    path('', include('dashboard.functions-urls')),
    path('', include('assignment.functions-urls')),
]


urlpatterns += i18n_patterns(
    path('', include('main.urls')),
    path('', include('student.urls')),
    path('', include('dashboard.urls')),
    path('', include('assignment.urls')),
) + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

urlpatterns = urlpatterns+static(settings.MEDIA_URL,
document_root=settings.MEDIA_ROOT)


handler404 = 'main.views.error_404'