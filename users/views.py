from django.core.exceptions import ValidationError, PermissionDenied
from django.forms import model_to_dict
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .forms import SignUpForm, EditUserForm, LoginForm, CommentForm
from .models import Comment
from articles.models import Article

from datetime import datetime

from faker import Faker


def prev_page(request):
	# sets redirect url to previous page
	next = request.GET.get('next')
	if not next:
		next = 'articles'
	return next


class SignUpView(View):

	def get(self, request):
		form = SignUpForm()
		return render(request, 'sign_up.html', {'form': form, 'title': 'Zarejestruj się'})

	def post(self, request):
		form = SignUpForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password1 = form.cleaned_data['password1']
			password2 = form.cleaned_data['password2']

			if password1 == password2:
				User.objects.create_user(username, email, password1)
				user = authenticate(username=username, password=password1)
				login(request, user)

				return redirect(prev_page(request))
			else:
				# passwords doesn't match
				raise ValidationError('Hasła muszą się ze sobą zgadzać')



class LoginView(View):

	def post(self, request):
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			raw_password = form.cleaned_data['password']

			user = authenticate(username=username, password=raw_password)
			login(request, user)

			return redirect(prev_page(request))


class LogoutView(View):

	def get(self, request):
		logout(request)
		return redirect(prev_page(request))


class ModifyUserView(View):

	def get(self, request):
		form = EditUserForm(initial={
			'username': request.user.username,
			'email': request.user.email,
		})
		return render(request, 'sign_up.html', {'form': form, 'title': 'Edytuj profil'})

	def post(self, request):
		form = EditUserForm(request.POST)
		user = User.objects.get(id=request.user.id)

		if form.is_valid():
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password1 = form.cleaned_data['password1']
			password2 = form.cleaned_data['password2']
			old_password = form.cleaned_data['old_password']

			if user.check_password(old_password):
				if username:
					user.username = username
				if email:
					user.email = email
				if password1 or password2:
					if password1 == password2:
						user.set_password(password1)
					else:
						# passwords doesn't match
						raise ValidationError('Nowe hasła muszą się ze sobą zgadzać.')
				user.save()

				user = authenticate(username=username, password=password1)
				login(request, user)

				return redirect(prev_page(request))
			else:
				# wrong current password
				raise ValidationError('Błędne, aktualne hasło.')


class SendCommentView(LoginRequiredMixin, View):

	def post(self, request):
		form = CommentForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect(prev_page(request))


class ModifyCommentView(LoginRequiredMixin, View):

	def get(self, request, comment_id):
		comment = Comment.objects.get(id=comment_id)
		form = CommentForm(initial=model_to_dict(comment))
		#form's action url
		action = redirect('modify-comment', comment_id=comment_id).url
		action += f'?next={request.GET.get("next")}'
		ctx = {
			'form': form,
			'title': 'Edytuj komentarz',
			'action': action
		}
		return render(request, 'creation_form.html', ctx)

	def post(self, request, comment_id):
		comment = Comment.objects.get(id=comment_id)
		user = request.user
		form = CommentForm(request.POST, instance=comment)
		if not (user.is_staff and not comment.author.is_staff or user == comment.author or user.is_superuser):
			# only superuser, author, or staff (when author is not another staff)
			# can modify and delete
			raise PermissionDenied()
		if form.is_valid():
			comment.modification_date = datetime.now()
			form.save()
			return redirect(prev_page(request))


class DeleteCommentView(LoginRequiredMixin, View):

	def get(self, request, comment_id):
		comment = Comment.objects.get(id=comment_id)
		user = request.user
		if not (user.is_staff and not comment.author.is_staff or user == comment.author or user.is_superuser):
			# only superuser, author, or staff (when author is not another staff)
			# can modify and delete
			raise PermissionDenied()
		comment.delete()
		return redirect(prev_page(request))


class AddFakeUsers(UserPassesTestMixin, View):

	def test_func(self):
		return self.request.user.is_superuser

	def get(self, request):
		for x in range(1, 11):
			User.objects.create_user(f'user{x}', f'user{x}@gmail.com', '123')
		for x in range(1, 3):
			User.objects.create_user(f'mod{x}', f'mod{x}@gmail.com', '123', is_staff=True)
		return HttpResponse('Zrobione')
