from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView


class LandingPage(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('runapp:homepage')
        return render(request, 'runapp/landing_page.html')


class HomepageView(TemplateView):
    template_name = 'runapp/homepage.html'
