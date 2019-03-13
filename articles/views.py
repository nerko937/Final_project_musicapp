from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import PermissionDenied
from django.forms.models import model_to_dict
from tqdm import trange

from .models import Article
from .forms import CreateArticleForm
from users.forms import CommentForm
from users.views import prev_page
from users.models import Comment

import random
from datetime import datetime

from faker import Faker


class ArticlesView(View):

	def get(self, request):
		article_list = Article.objects.all().order_by('-creation_date')
		page = request.GET.get('page', 1)

		paginator = Paginator(article_list, 10)
		try:
			articles = paginator.page(page)
		except PageNotAnInteger:
			articles = paginator.page(1)
		except EmptyPage:
			articles = paginator.page(paginator.num_pages)

		return render(request, 'articles.html', {'articles': articles})



class ArticleView(View):

	def get(self, request, article_id):
		article = Article.objects.get(id=article_id)
		comments = Comment.objects.filter(article=article).order_by('creation_date')
		form = CommentForm(initial={
			'article': article,
			'author': request.user
		})
		ctx = {
			'article': article,
			'comments': comments,
			'form': form,
			'action': redirect('send-comment').url
		}
		#edit_form = CreateArticleForm(initial=model_to_dict(article))
		return render(request, 'article.html', ctx)


class CreateArticleView(UserPassesTestMixin, View):

	def test_func(self):
		return self.request.user.is_staff or self.request.user.is_superuser

	def get(self, request):
		form = CreateArticleForm(initial={'author': request.user})
		ctx = {
			'form': form,
			'title': 'Tworzenie nowego artykułu',
		}
		return render(request, 'creation_form.html', ctx)

	def post(self, request):
		form = CreateArticleForm(request.POST, request.FILES)
		if form.is_valid():
			article = form.save()
			return redirect('article', article_id=article.id)


class ModifyArticleView(UserPassesTestMixin, View):

	def test_func(self):
		return self.request.user.is_staff or self.request.user.is_superuser

	def get(self, request, article_id):
		article = Article.objects.get(id=article_id)
		form = CreateArticleForm(initial=model_to_dict(article))
		ctx = {
			'form': form,
			'title': 'Edycja artykułu'
		}
		if article.author != request.user and not request.user.is_superuser:
			# staff members can modify only their own articles
			raise PermissionDenied()
		return render(request, 'creation_form.html', ctx)

	def post(self, request, article_id):
		article = Article.objects.get(id=article_id)
		form = CreateArticleForm(data=request.POST, files=request.FILES, instance=article)
		if form.is_valid():
			article.modification_date = datetime.now()
			form.save()
			return redirect('article', article_id=article.id)


class DeleteArticleView(UserPassesTestMixin, View):

	def test_func(self):
		return self.request.user.is_staff or self.request.user.is_superuser

	def get(self, request, article_id):
		article = Article.objects.get(id=article_id)
		if article.author != request.user and not request.user.is_superuser:
			# staff members can delete only their own articles
			raise PermissionDenied()
		article.delete()
		return redirect(prev_page(request))


class AddArticles(UserPassesTestMixin, View):

	def test_func(self):
		return self.request.user.is_superuser

	# adds fake articles to db
	def get(self, request):
		fake = Faker('pl_PL')
		mods = User.objects.filter(username__contains='mod')
		users = User.objects.all()
		# articles
		for _ in trange(0, 50):
			content = ''
			for _ in range(random.randint(3, 8)):
				content += f'<p>{fake.text()}</p>'
			article = Article.objects.create(
				author=random.choice(mods),
				title=fake.sentence(),
				content=content
			)
			# comments
			for _ in range(1, random.randint(1, 10)):
				Comment.objects.create(
					author=random.choice(users),
					comment=fake.sentence(),
					article=article
				)
		return render(request, 'base.html')
