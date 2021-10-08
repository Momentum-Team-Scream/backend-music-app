"""music URL Configuration

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
from api import views as api_views
from rest_framework.routers import SimpleRouter

router = SimpleRouter()
router.register(r'note', api_views.NoteViewSet)
router.register(r'practices', api_views.PracticeLogViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/users/', api_views.DjoserUserViewSet.as_view({'get': 'list'}), name='register-new-user'),
    path('auth/users/me/', api_views.ProfileViewSet.as_view(), name='profile'),
    path('api/upcoming/', api_views.LessonViewSet.as_view(), name='lesson-list'),
    path('api/lessons/', api_views.LessonViewSet.as_view(), name='lesson-add'), 
    path('api/lessons/<int:pk>/', api_views.LessonDetailViewSet.as_view(), name='lesson-detail'), 
    path('instructor/studio/', api_views.list_students, name='instructor-studio'),
    path('api/user/<int:pk>/', api_views.SharedProfileViewSet.as_view({'get': 'retrieve'}), name='shared-profile')
]
