from django import forms
from django.contrib.auth.forms import UserCreationForm as DjangoUserCreationForm
from django.contrib.auth.models import User

class UserCreationForm(DjangoUserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
        })
    )

    class Meta(DjangoUserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
