from django.shortcuts import render, redirect
from django.views import View


class LandingPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('runapp:homepage')
        return render(request, 'runapp/landing_page.html')


class HomePageView(View):
    def get(self, request):
        return render(request, 'runapp/homepage.html')
