from django.http import HttpResponseRedirect
from django.urls import reverse


class AuthRequiredMiddleware(object): #TODO add to middleware
    def process_request(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('landing_page')) #TODO make login page
        return None
