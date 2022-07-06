from django.shortcuts import render


def index(request):
    return render(request, "index.html")


def error_404_view(request, exception):
    return render(request, "index.html")
