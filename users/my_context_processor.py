from .forms import LoginForm


def current_url(request):
	return {'next': f'?next={request.get_full_path()}'}


def login_form(request):
	return {'login_form': LoginForm()}
