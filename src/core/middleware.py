from django.http import HttpResponseRedirect
from django.urls import reverse


class AuthRequiredMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        excludedUris = (
            request.path != "/user/login/" and request.path != "/user/signup/"
        )

        if not request.user.is_authenticated and excludedUris:
            return HttpResponseRedirect(reverse("login"))

        response = self.get_response(request)

        return response
