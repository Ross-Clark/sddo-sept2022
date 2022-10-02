from django.shortcuts import redirect, render


def index(request):
    if request.user.is_authenticated:
        return redirect("/choose-your-own-device")
    else:
        return redirect("/user/login")


def about(request):
    return render(request, "about.html")
