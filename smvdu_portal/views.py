from django.shortcuts import render_to_response
from django.shortcuts import render

def about (request):
	if 'uname' in request.session:
		return render(request,'courses.html',{'logged':request.session['info_dic']})
	return render(request,'courses.html')