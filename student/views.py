from django.shortcuts import render

# Create your views here.
from django.shortcuts import render_to_response
import datetime
def home(request):
	now = datetime.datetime.now()
	return render_to_response('login_register.html', {'current_date': now})