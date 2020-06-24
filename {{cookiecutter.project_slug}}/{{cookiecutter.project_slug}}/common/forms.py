from django.forms import ModelForm
from common.models import User
from django.contrib.auth.forms import UserCreationForm


# Create the form class.

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']
