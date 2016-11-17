import json

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse, Http404

from app.forms.user_registration import UserForm
from app.forms.login import LoginForm
from app.services.user import user_is_member

def home(request):
	if request.method == 'POST':
		response = {}
		data = {}
		user_form = UserForm(data=request.POST)

		if user_form.is_valid():
			user = user_form.save()
			user.set_password(user.password)
			user.save()

			user = authenticate(username=request.POST['username'], password=request.POST['password'])
			login(request, user)

			data['url'] = "http://%s" % request.get_host()
			response['data'] = data
			response['success'] = 'success'

		else:
			errors = user_form.errors.as_json()
			data['errors'] = errors
			response['data'] = data
			response['failed'] = 'failed'

		return HttpResponse(json.dumps(response), content_type='application/json')

	elif request.user.is_authenticated and request.user.username != '':
		#if user_is_member(request.user):
		return render(request, 'dashboard.html')

		#else:
			#return HttpResponseRedirect('/register')

	user_form = UserForm()
	login_form = LoginForm()
	return render(request, 'public/home.html', {'user_form' : user_form, 'login_form' : login_form})

def test(request):
	user_objects = User.objects.all()
	context = {'user_objects': user_objects}
	return render(request, 'groupTest.html', context)