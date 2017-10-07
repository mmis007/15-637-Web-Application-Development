from django import forms
from .models import *
from django.contrib.auth.models import User


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)

    def clean(self):
        cleaned_data = super(CommentForm, self).clean()
        if cleaned_data == {}:
            print("no")
            raise forms.ValidationError('You must write something to post.')

        return cleaned_data

    def clean_text(self):
        text = self.cleaned_data.get('text')
        print('hi')
        print(text)
        if not text:
            raise forms.ValidationError('You must write comment to post.')
        return text


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('text',)

    def clean(self):
        cleaned_data = super(PostForm, self).clean()
        return cleaned_data

    def clean_text(self):
        text = self.cleaned_data.get('text')
        if not text:
            raise forms.ValidationError('You must write something to post.')
        return text


class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=20)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=100)
    password1 = forms.CharField(max_length=200,
                                label='Password',
                                widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=200,
                                label='Confirm password',
                                widget=forms.PasswordInput())

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # We must return the cleaned data we got from our parent.
        return cleaned_data

    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # We must return the cleaned data we got from the cleaned_data
        # dictionary
        return username


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name')

    def clean(self):
        cleaned_data = super(UserForm, self).clean()

        return cleaned_data


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('bio', 'age', 'photo')
        widgets = {'photo': forms.FileInput()}

    def clean(self):

        cleaned_data = super(ProfileForm, self).clean()
        print(cleaned_data)
        return cleaned_data

    def clean_age(self):
        age = (self.cleaned_data.get('age'))
        if not age:
            age = 0
        return age


