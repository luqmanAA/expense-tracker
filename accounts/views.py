from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View


# Define a class-based view for welcoming users
class UserWelcomeView(LoginRequiredMixin, View):
    # Redirect users to the login page if they are not authenticated
    login_url = "/"

    # Handle GET requests to the view
    def get(self, request):
        # Retrieve the user's first name, default to an empty string if not present
        name = request.user.first_name if request.user.first_name else ''

        # Append the user's last name to the name, with a space if the last name is present
        name += ' ' + request.user.last_name if request.user.last_name else ''

        # Render the 'welcome.html' template with the user's email and full name as context
        return render(
            request,
            "welcome.html",  # Template to render
            context={  # Context data to pass to the template
                'email': request.user.email,  # User's email
                'name': name,  # Full name of the user
            }
        )
