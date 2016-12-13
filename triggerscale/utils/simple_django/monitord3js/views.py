from django.shortcuts import render


def index(request):
    response = render(request, "monitord3js/index.html", context={})
    return response




