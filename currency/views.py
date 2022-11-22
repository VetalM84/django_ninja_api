from django.shortcuts import render


def index(request):
    """Index file."""
    return render(request, "index.html")
