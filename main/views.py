from django.shortcuts import redirect, render
from django.urls import reverse


def index_view(request):
    if request.user.is_authenticated:
        return redirect(reverse("accounts:welcome"))

    return render(request, "index.html")
