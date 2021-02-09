from django.shortcuts import render

# Create your views here.

def home_view(request, *args, **kwargs):
	kontextus = {
		"a": 123,
		"b": "blablabla",
		"l": [1,3,5,7,9],
	}

	print(f"A kontextusban az a értéke: {kontextus['a']}")


	return render(request, "home.html", kontextus) 
