from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView


class LandingPage(View):
    """Display application landing page."""

    def get(self, request):
        """Display landing page or redirect to homepage.

        Display landing page for non-authenticated users only,
        redirect logged in users to the application homepage.
        """
        if request.user.is_authenticated:
            return redirect('runapp:homepage')
        return render(request, 'runapp/landing_page.html')


class HomepageView(TemplateView):
    """Display application homepage."""
    template_name = 'runapp/homepage.html'
