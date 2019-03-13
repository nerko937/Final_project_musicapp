from.models import GENRES


def genres(request):
	return {'genres': [g[0] for g in GENRES]}