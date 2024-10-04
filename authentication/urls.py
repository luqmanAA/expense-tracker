from django.urls import path, include

from authentication.views import LogoutView


urlpatterns = [
    path('logout', LogoutView.as_view(), name='logout'),
    path('oauth2/', include('django_auth_adfs.urls')),
]
