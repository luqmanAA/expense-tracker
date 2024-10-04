from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View


# Define a class-based view for logging out users
class LogoutView(View):
    # Handle GET requests to the view
    def get(self, request):
        # Log out the user by calling the logout function
        logout(request)

        # Redirect the user to the 'index' URL after logging out
        return redirect(reverse('index'))  # Reverse resolves the URL pattern named 'index'
