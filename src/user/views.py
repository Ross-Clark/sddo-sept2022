from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

class LogonView(View):

    template_name = 'logon.html'

    def get(self, request):

        return render(request,self.template_name)

    def post(self, request):

        return render(request,self.template_name)


class SignUpView(View):

    template_name = 'signup.html'

    def get(self, request):

        return render(request,self.template_name)

    def post(self, request):

        return render(request,self.template_name)


class ProfileView(View):

    template_name = 'profile.html'

    def get(self, request):

        return render(request,self.template_name)

    def post(self, request):

        return render(request,self.template_name)
