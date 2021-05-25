from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView

from runapp.forms import UserForm, TrainingPlanForm, SelectCurrentPlanForm, \
    TrainingForm
from runapp.models import TrainingPlan, Training


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
            return redirect(training_plan)

        return render(request, self.template_name, {'form': form})


class TrainingPlanEditView(View):
    """View for editing an existing training plan."""
    form_class = TrainingPlanForm
    template_name = 'runapp/training_plan_edit.html'

    def get(self, request, pk):
        """Display the form for editing the training plan."""
        training_plan = get_object_or_404(TrainingPlan, pk=pk)
        training_plan.confirm_owner(request.user)
        form = self.form_class(instance=training_plan)
        return render(request, self.template_name,
                      {'form': form, 'plan_id': pk})

    def post(self, request, pk):
        """Edit the selected training plan."""
        training_plan = get_object_or_404(TrainingPlan, pk=pk)
        form = self.form_class(request.POST, instance=training_plan)
        if form.is_valid():
            form.save()
            return redirect(training_plan)

        return render(request, self.template_name,
                      {'form': form, 'plan_id': pk})


class TrainingPlanDetailsView(View):
    """View for displaying details about the training plan."""

    def get(self, request, pk):
        """Display information about the selected training plan."""
        training_plan = get_object_or_404(TrainingPlan, pk=pk)
        training_plan.confirm_owner(request.user)
        return render(request, 'runapp/training_plan_details.html',
                      {'training_plan': training_plan})


class TrainingPlanListView(View):
    """View for displaying the list of user training plans."""

    def get(self, request):
        """Display all user training plans."""
        training_plans = TrainingPlan.objects.filter(owner=request.user)
        return render(request, 'runapp/training_plan_list.html',
                      {'training_plans': training_plans})


class SelectCurrentTrainingPlanView(View):
    """View for selecting the current training plan."""
    form_class = SelectCurrentPlanForm
    template_name = 'runapp/select_current_training_plan.html'

    def get(self, request):
        """Display the form for choosing the current training plan."""
        form = self.form_class(request.user)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        """Set the selected training plan as current."""
        form = self.form_class(request.user, data=request.POST)
        if form.is_valid():
            plan_id = form.cleaned_data.get('current_plan')
            TrainingPlan.set_current(plan_id)
            return redirect('runapp:training_plan_list')

        return render(request, self.template_name, {'form': form})


class TrainingCreateView(View):
    """View for creating a new training."""
    form_class = TrainingForm
    template_name = 'runapp/training_create.html'

    def get(self, request, plan_pk):
        """Display the form for creating a new training."""
        training_plan = get_object_or_404(TrainingPlan, pk=plan_pk)
        training_plan.confirm_owner(request.user)
        form = self.form_class()
        context = {'form': form, 'training_plan': training_plan}
        return render(request, self.template_name, context)

    def post(self, request, plan_pk):
        """Create a new training."""
        training_plan = get_object_or_404(TrainingPlan, pk=plan_pk)
        form = self.form_class(request.POST)
        if form.is_valid():
            form.instance.training_plan = training_plan
            form.save()
            return redirect(training_plan)

        context = {'form': form, 'training_plan': training_plan}
        return render(request, self.template_name, context)


class TrainingEditView(View):
    """View for editing a scheduled training."""
    form_class = TrainingForm
    template_name = 'runapp/training_create.html'

    def get(self, request, pk):
        """Display the form for editing the training."""
        training = get_object_or_404(Training, pk=pk)
        plan = training.training_plan
        plan.confirm_owner(request.user)
        form = self.form_class(instance=training)
        context = {'form': form, 'training_plan': plan}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        """Edit the selected training."""
        training = get_object_or_404(Training, pk=pk)
        plan = training.training_plan
        form = self.form_class(data=request.POST, instance=training)
        if form.is_valid():
            form.save()
            return redirect(plan)

        context = {'form': form, 'training_plan': plan}
        return render(request, self.template_name, context)
