'''Collection of forms for user app'''
from django import forms

from .models import CustomUser


class CustomUserForm(forms.ModelForm):
    '''CustomUser form'''

    def __init__(self, *args, **kwargs):
        '''Override init for the user form'''
        super().__init__(*args, **kwargs)
        if not self.instance._state.adding:
            self.fields['password'].required = False

    def save(self, commit: bool = True) -> CustomUser:
        '''Override save method to handle user's password'''
        if not self.instance._state.adding: # pylint: disable=W0212
            password = self.cleaned_data.pop('password')
            CustomUser.objects.filter(
                pk=self.instance.pk).update(**self.cleaned_data)

            user = CustomUser.objects.get(pk=self.instance.pk)
            if password:
                user.set_password(password)
                user.save()

        else:
            user = super().save(commit=False)
            password = self.cleaned_data.pop('password')
            if password:
                user.set_password(password)
            if commit:
                user.save()

        return user


    class Meta:
        '''Configuration of the form'''
        model = CustomUser
        fields = (
            'email', 'username', 'password', 'is_active', 'role'
        )
        widgets = {
            'password': forms.PasswordInput()
        }
