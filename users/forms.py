from django import forms
from .models import Comment


class SignUpForm(forms.Form):

	username = forms.CharField(
		required=True,
		label='Nazwa użytkownika',
		max_length=155
	)
	email = forms.EmailField(
		required=True,
		label='Email'
	)
	password1 = forms.CharField(
		required=True,
		label='Nowe hasło',
		widget=forms.PasswordInput()
	)
	password2 = forms.CharField(
		required=True,
		label='Powtórz nowe hasło',
		widget=forms.PasswordInput()
	)


class EditUserForm(forms.Form):

	username = forms.CharField(
		required=False,
		label='Nazwa użytkownika',
		max_length=155
	)
	email = forms.EmailField(
		required=False,
		label='Email'
	)
	password1 = forms.CharField(
		required=False,
		label='Nowe hasło',
		widget=forms.PasswordInput()
	)
	password2 = forms.CharField(
		required=False,
		label='Powtórz nowe hasło',
		widget=forms.PasswordInput()
	)
	old_password = forms.CharField(
		required=True,
		label='Stare hasło',
		widget=forms.PasswordInput()
	)


class LoginForm(forms.Form):

	username = forms.CharField(
		required=True,
		max_length=155,
		widget=forms.TextInput(attrs={
			'placeholder': 'Nazwa użytkownika',
			'class': 'form-control mr-sm-2'
		})
	)
	password = forms.CharField(
		required=True,
		widget=forms.PasswordInput(attrs={
			'placeholder': 'Hasło',
			'class': 'form-control mr-sm-2'
		})
	)


class CommentForm(forms.ModelForm):

	class Meta:
		model = Comment
		exclude = ('modification_date', 'creation_date')
		widgets = {
			'article': forms.HiddenInput(),
			'band': forms.HiddenInput(),
			'album': forms.HiddenInput(),
			'song': forms.HiddenInput(),
			'author': forms.HiddenInput()
		}