from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from runapp.models import User, TrainingPlan, Training
from runapp.widget import DatePicker


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
        self.fields['current_plan'] = forms.ChoiceField(
            choices=user_plans, label='Choose your current plan')
