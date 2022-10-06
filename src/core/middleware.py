from django.http import HttpResponseRedirect
from django.urls import reverse
from core.urls import urlpatterns
import logging

logger = logging.getLogger(__name__)

class AuthRequiredMiddleware(object):
    '''
    Prevents unautherised users from accessing all pages
    except for the ones required to gain authentication 
    '''
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # Boolean to determine if the request is from one of the whitelisted URLS
        excludedUris = request.path != "/user/login/" and request.path != "/user/signup/"

        # Returns the user to the login page if the user is not authenticated
        # and is not on a whitelisted page
        # logs the attempt
        if not request.user.is_authenticated and excludedUris:
            url = self.validate_url(request.path)
            if url:
                logger.warning("anonymous user attempted to access site : %s",url)
            else:
                logger.warning("anonymous user attempted to access site : invalid page")

            return HttpResponseRedirect(reverse("login"))

        # Otherwise returns the regular response
        response = self.get_response(request)

        return response

    def validate_url(self,url):
        # search urlpatterns for url
        # return url if it matches else return None 
        for e in urlpatterns:
            if e.regex.match(url):
                return url
        return None
