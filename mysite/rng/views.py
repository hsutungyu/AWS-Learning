from django.http import HttpResponse

def index(request, number):
    return HttpResponse("Hello, world. You're at the index page of RNG.")