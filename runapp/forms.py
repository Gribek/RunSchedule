from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from runapp.models import User, TrainingPlan, Training, TrainingDiary
from runapp.widget import DatePicker
from runapp.calendar import get_date_today


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email']


class TrainingPlanForm(ModelForm):
    class Meta:
        model = TrainingPlan
        exclude = ['owner']
        widgets = {
            'start_date': DatePicker(),
            'end_date': DatePicker(),
        }
        labels = {
            'current_plan': 'Set as current plan'
        }


class TrainingForm(ModelForm):
    class Meta:
        model = Training
        exclude = ['completed', 'training_plan']
        widgets = {
            'date': DatePicker(),
        }


class SelectCurrentPlanForm(forms.Form):
    """Form for selecting the current training plan."""

    def __init__(self, user, **kwargs):
        super(SelectCurrentPlanForm, self).__init__(**kwargs)
        user_plans = [(plan.id, plan.name) for plan in
                      TrainingPlan.objects.filter(owner=user)]
        current_plan = TrainingPlan.get_current(user)
        initial_value = current_plan.pk if current_plan else None
        self.fields['current_plan'] = forms.ChoiceField(
            choices=user_plans, label='Choose your current plan',
            initial=initial_value)


class DiaryEntryForm(ModelForm):
    class Meta:
        model = TrainingDiary
        exclude = ['user', 'average_speed']
        widgets = {
            'date': DatePicker(),
        }

    def clean_date(self):
        """Check that the training date is not later than today."""
        date = self.cleaned_data['date']
        if get_date_today() < date:
            self.add_error('date', 'You cannot add an entry for training '
                                   'that has not yet taken place')
        return date
