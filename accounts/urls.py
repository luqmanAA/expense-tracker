from django.urls import path

from accounts.views import UserWelcomeView

app_name = 'accounts'

urlpatterns = [
    path('', UserWelcomeView.as_view(), name='welcome'),
]
