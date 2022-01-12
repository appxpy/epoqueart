from django.shortcuts import render

def home(request):
	return render(request, 'main/coming_soon.html')

def minecraft(request):
	return render(request, 'main/minecraft.html')

def projects(request):
	return render(request, 'main/dev.html')

def handler404(request, exception):
	return render(request, 'main/404.html', status=404)

def handler500(request):
	return render(request, 'main/500.html', status=500)

def handler401(request):
	return render(request, 'main/401.html', status=401)

def handler400(request, exception):
	return render(request, 'main/400.html', status=400)

def handler403(request, exception):
	return render(request, 'main/403.html', status=403)
