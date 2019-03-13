from django import forms

from .models import Article


class CreateArticleForm(forms.ModelForm):

	class Meta:
		model = Article
		exclude = ('modification_date', 'creation_date')
		widgets = {'author': forms.HiddenInput(), 'content': forms.HiddenInput()}