from django import forms
from authentication.models import USER_TYPE, UserProfile
from django.contrib.auth import authenticate


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': 'inputBox', 'placeholder': 'Enter password'}))
    password_2 = forms.CharField(
        label='', widget=forms.PasswordInput(attrs={'class': 'inputBox', 'placeholder': 'Confirm password'}))
    user_type = forms.ChoiceField(
        choices=USER_TYPE, widget=forms.Select(attrs={'class': 'choicesBox'}))

    class Meta:
        model = UserProfile
        fields = ['user_type', 'firstname', 'lastname', 'email', 'phonenumber']
        labels = {
            'firstname': '',
            'lastname': '',
            'email': '',
            'phonenumber': ''
        }
        widgets = {
            'firstname': forms.TextInput(attrs={'class': 'inputBox', 'placeholder': 'Enter first name'}),
            'lastname': forms.TextInput(attrs={'class': 'inputBox', 'placeholder': 'Enter last name'}),
            'email': forms.EmailInput(attrs={'class': 'inputBox', 'placeholder': 'Email Address'}),
            'phonenumber': forms.NumberInput(attrs={'class': 'inputBox', 'placeholder': 'Enter phone number'}),
        }

    def clean_email(self):
        '''
        Verify email is available.
        '''
        email = self.cleaned_data.get('email')
        qs = UserProfile.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean(self):
        '''
        Verify both passwords match.
        '''
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        print(password)
        password_2 = cleaned_data.get("password_2")
        print(password_2)
        if password is not None and password != password_2:
            self.add_error("password_2", "Your passwords must match")
        return cleaned_data

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.user_type = self.cleaned_data["user_type"]
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class AccountAuthenticationForm(forms.ModelForm):
    """
      Form for Logging in  users
    """
    password = forms.CharField(label='', widget=forms.PasswordInput(
        attrs={'class': 'inputBox', 'placeholder': 'Enter password'}))

    class Meta:
        model = UserProfile
        fields = ('email', 'password')
        labels = {'email': ''}
        widgets = {
            'email': forms.TextInput(attrs={'class': 'inputBox', 'placeholder': 'Email Address'}),
            'password': forms.TextInput(),
        }

    def __init__(self, *args, **kwargs):
        """
          specifying styles to fields 
        """
        super(AccountAuthenticationForm, self).__init__(*args, **kwargs)
        for field in (self.fields['email'], self.fields['password']):
            field.widget.attrs.update({'class': 'inputBox '})

    def clean(self):
        if self.is_valid():

            email = self.cleaned_data.get('email')
            password = self.cleaned_data.get('password')
            if not authenticate(email=email, password=password):
                raise forms.ValidationError('Invalid Login')
