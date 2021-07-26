from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import PermissionDenied, ValidationError
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

    def clean(self):
        """Validate plan start and end dates."""
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        if end_date < start_date:
            raise ValidationError(
                'The start date cannot be later than the end date')
        return cleaned_data


class TrainingForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(TrainingForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Training
        exclude = ['completed', 'training_plan']
        widgets = {
            'date': DatePicker(attrs={'class': 'form-control'}),
            'main_training': forms.TextInput(attrs={'class': 'form-control'}),
            'additional_training': forms.TextInput(
                attrs={'class': 'form-control'}),
        }

    def clean(self):
        """Validate ownership of the training plan.

        Make sure the user does not make changes to another user's
        training plan.
        """
        cleaned_data = super().clean()
        owner = self.instance.training_plan.owner
        if self.user != owner:
            raise PermissionDenied
        return cleaned_data

    def clean_date(self):
        date = self.cleaned_data['date']
        training_plan = self.instance.training_plan

        if training_plan.training_set.filter(date=date):
            self.add_error('date',
                           'You already have training planned for that day.')
        if date < training_plan.start_date:
            self.add_error('date', 'The date of the training cannot be earlier'
                                   ' than the  training plan start date')
        if date > training_plan.end_date:
            self.add_error('date', 'The date of the training cannot be later'
                                   ' than the training plan end date.')
        return date


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
        self.fields['current_plan'].widget.attrs.update(
            {'class': 'form-control'})


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

    def clean_training_distance(self):
        """Check that the training distance is greater than zero."""
        distance = self.cleaned_data['training_distance']
        if not distance > 0:
            self.add_error('training_distance',
                           'Training distance must be greater than zero')
        return distance

    def clean_training_time(self):
        """Check that the training time is greater than zero."""
        time = self.cleaned_data['training_time']
        if not time > 0:
            self.add_error('training_time',
                           'Training time must be greater than zero')
        return time
