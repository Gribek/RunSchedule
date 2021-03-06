from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import TemplateView

from runapp.calendar import TrainingCalendar, get_date_today, str_to_datetime
from runapp.forms import (UserForm, TrainingPlanForm, SelectCurrentPlanForm,
                          TrainingForm, DiaryEntryForm)
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


class HomepageView(LoginRequiredMixin, TemplateView):
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


class TrainingPlanCreateView(LoginRequiredMixin, View):
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


class TrainingPlanEditView(LoginRequiredMixin, View):
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


class TrainingPlanDetailsView(LoginRequiredMixin, View):
    """View for displaying details about the training plan."""

    def get(self, request, pk):
        """Display information about the selected training plan."""
        training_plan = get_object_or_404(TrainingPlan, pk=pk)
        training_plan.confirm_owner(request.user)
        context = {'training_plan': training_plan, 'today': get_date_today()}
        return render(request, 'runapp/training_plan_details.html', context)


class TrainingPlanListView(LoginRequiredMixin, View):
    """View for displaying the list of user training plans."""

    def get(self, request):
        """Display all user training plans."""
        training_plans = TrainingPlan.objects.filter(owner=request.user)
        return render(request, 'runapp/training_plan_list.html',
                      {'training_plans': training_plans})


class SelectCurrentTrainingPlanView(LoginRequiredMixin, View):
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
            today = get_date_today()
            return redirect('runapp:calendar', today.month, today.year)

        return render(request, self.template_name, {'form': form})


class TrainingCreateView(LoginRequiredMixin, View):
    """View for creating a new training."""
    form_class = TrainingForm
    template_name = 'runapp/training_create.html'

    def get(self, request, plan_pk):
        """Display the form for creating a new training."""
        training_plan = get_object_or_404(TrainingPlan, pk=plan_pk)
        training_plan.confirm_owner(request.user)
        date = str_to_datetime(request.GET.get('date'))
        form = self.form_class(initial={'date': date})
        context = {'form': form, 'training_plan': training_plan, 'date': date}
        return render(request, self.template_name, context)

    def post(self, request, plan_pk):
        """Create a new training."""
        training_plan = get_object_or_404(TrainingPlan, pk=plan_pk)
        form = self.form_class(request.POST, user=request.user)
        form.instance.training_plan = training_plan
        if form.is_valid():
            training = form.save()
            if request.GET.get('date'):
                return redirect('runapp:calendar', training.date.month,
                                training.date.year)
            return redirect(training_plan)

        context = {'form': form, 'training_plan': training_plan}
        return render(request, self.template_name, context)


class TrainingEditView(LoginRequiredMixin, View):
    """View for editing a scheduled training."""
    form_class = TrainingForm
    template_name = 'runapp/training_create.html'

    def get(self, request, pk):
        """Display the form for editing the training."""
        training = get_object_or_404(Training, pk=pk)
        plan = training.training_plan
        plan.confirm_owner(request.user)
        date = str_to_datetime(request.GET.get('date'))
        form = self.form_class(instance=training)
        context = {'form': form, 'training_plan': plan, 'date': date}
        return render(request, self.template_name, context)

    def post(self, request, pk):
        """Edit the selected training."""
        training = get_object_or_404(Training, pk=pk)
        plan = training.training_plan
        form = self.form_class(data=request.POST, instance=training,
                               user=request.user)
        if form.is_valid():
            form.save()
            if request.GET.get('date'):
                return redirect('runapp:calendar', training.date.month,
                                training.date.year)
            return redirect(plan)

        context = {'form': form, 'training_plan': plan}
        return render(request, self.template_name, context)


class TrainingDeleteView(LoginRequiredMixin, View):
    """View for deleting a scheduled training."""

    def post(self, request, pk):
        """Delete the selected training."""
        training = get_object_or_404(Training, pk=pk)
        plan = training.training_plan
        plan.confirm_owner(request.user)
        training.delete()
        return redirect(plan)


class CurrentPlanCalendarView(LoginRequiredMixin, View):
    """Display a monthly calendar with the user's current plan."""

    def get(self, request, month, year):
        """Display a calendar for the given month."""
        current_plan = TrainingPlan.get_current(request.user)
        context = {'training_plan': current_plan}
        if current_plan is not None:
            calendar = TrainingCalendar(current_plan, month, year)
            monthly_calendar = calendar.formatmonth(year, month)
            previous_month, next_month = calendar.previous_and_next_month()
            context.update({
                'monthly_calendar': monthly_calendar,
                'previous_month': previous_month,
                'next_month': next_month,
            })
        return render(request, 'runapp/current_plan_calendar.html', context)


class TrainingDiaryView(LoginRequiredMixin, View):
    """View for displaying a training diary."""

    def get(self, request):
        """Display user training diary."""
        user = request.user
        entries = user.trainingdiary_set.all().order_by('date')
        return render(request, 'runapp/training_diary.html',
                      {'entries': entries})


class DiaryEntryCreateView(LoginRequiredMixin, View):
    """View for adding a new entry to the training diary."""
    form_class = DiaryEntryForm
    template_name = 'runapp/diary_entry_create.html'

    def get(self, request, training_pk):
        """Display the form for creating a new diary entry."""
        training = get_object_or_404(Training, pk=training_pk)
        plan = training.training_plan
        plan.confirm_owner(request.user)
        if training.completed:
            return redirect(plan)
        form = self.form_class(initial={
            'date': training.date,
            'training_information': training.training_information()
        })
        context = {'form': form, 'plan_pk': plan.id}
        return render(request, self.template_name, context)

    def post(self, request, training_pk):
        """Create a new diary entry."""
        training = get_object_or_404(Training, pk=training_pk)
        plan = training.training_plan
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.average_speed = form.cleaned_data.get(
                'training_distance') / form.cleaned_data.get('training_time')
            form.save()
            training.completed = True
            training.save()
            return redirect(plan)
        context = {'form': form, 'plan_pk': plan.id}
        return render(request, self.template_name, context)
