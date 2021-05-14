from django.contrib.auth.forms import UserCreationForm

from runapp.models import User


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email']
