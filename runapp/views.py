from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView

from runapp.forms import UserForm, TrainingPlanForm
from runapp.models import TrainingPlan


class LandingPageView(View):
    """View for displaying application landing page."""

    def get(self, request):
        """Display landing page or redirect to homepage.

        Display landing page for non-authenticated users only,
        redirect logged in users to the application homepage.
        """
        if request.user.is_authenticated:
            return redirect('runapp:homepage')
        return render(request, 'runapp/landing_page.html')


class HomepageView(TemplateView):
    """View for displaying application homepage."""
    template_name = 'runapp/homepage.html'


class RegisterUserView(View):
    """View for registering a new user."""
    form_class = UserForm
    template_name = 'runapp/register_user.html'

    def get(self, request):
        """Display the registration form."""
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Create a new user."""
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('runapp:login')

        return render(request, self.template_name, {'form': form})


class TrainingPlanCreateView(View):
    """View for creating a new training plan."""
    form_class = TrainingPlanForm
    template_name = 'runapp/training_plan_create.html'

    def get(self, request):
        """Display the form for creating a new training plan."""
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Create a new training plan."""
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.owner = request.user
            training_plan = form.save()
            if training_plan.current_plan:
                pass  # TODO: implement set plan as current
            return redirect('runapp:homepage')  # TODO: redirect to plan list
        return render(request, self.template_name, {'form': form})


class TrainingPlanDetailsView(View):
    """View for displaying details about the training plan."""

    def get(self, request, pk):
        """Display information about the selected training plan."""
        training_plan = get_object_or_404(TrainingPlan, pk=pk)
        training_plan.confirm_owner(request.user)
        return render(request, 'runapp/training_plan_details.html',
                      {'training_plan': training_plan})
