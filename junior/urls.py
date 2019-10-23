"""junior URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.views.decorators.cache import cache_page

from catalog import views


urlpatterns = [

    path('', cache_page(60*5)(views.IndexView.as_view()), name='home'),
    path('contact/', cache_page(60*5)(views.ContactView.as_view()), name='contact'),
    path('result-list/', views.ResultListView.as_view(), name='result'),
    path('essay/<slug:slug>/', views.EssayDetailView.as_view(), name='essay'),

    path('summernote/', include('django_summernote.urls')),
    path('admin/', admin.site.urls),
    path('robots.txt', views.robots_view)

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
