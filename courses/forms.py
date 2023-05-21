from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("name", "email", "username", 'telephone_number', 'address', 'password1', 'password2')
        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control border-bottom', 'id': 'name'}),
        # }

class UserChangingForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("profile_image", "name", "username", "email", "gender", "dob", "address", "telephone_number")