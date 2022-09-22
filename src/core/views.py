from django.shortcuts import redirect

def index(request):
    return redirect('/choose-your-own-device')