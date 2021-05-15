from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from runapp.models import User, TrainingPlan
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
