from django.shortcuts import render_to_response
from django.shortcuts import render

def about (request):
	return render(request,'about.html')