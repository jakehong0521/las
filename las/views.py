from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core import serializers
from django.views import View
from las.models import *
from .forms import *
import json

# Create your views here.
def index(request):
	return render(request, 'las/index.html')

def category(request):
	if (request.method == "POST"):
		profiles = Profile.objects.filter(field=request.POST['field'].lower()).annotate(Count('post')).order_by('-post__count')
		response = list(profiles.values('username', 'post__count', 'title', 'company'))
		i = 0
		while i < profiles.count():
			response[i]['post__count'] = profiles[i].post__count
			i += 1
		return HttpResponse(json.dumps(response), content_type='application/json')
	else:
		fields = []
		for field in Profile._meta.get_field('field').choices:
			fields.append(field[1])
		return render(request, 'las/category.html', {'fields': fields})

def guide(request):
	return render(request, 'las/guide.html')

def signinup(request):
	userForm = UserForm(None)
	profileForm = ProfileForm(None)
	return render(request, 'las/signinup.html', {'userform': userForm, 'profileform': profileForm})

def signin(request):
	username = request.POST['username']
	password = request.POST['password']

	user = authenticate(username=username, password=password)

	if user is not None:
		login(request, user)
		return redirect('../')
	else:
		userForm = UserForm(None)
		profileForm = ProfileForm(None)
		return render(request, 'las/signinup.html', {'status': 'invalid', 'userform': userForm, 'profileform': profileForm})

def signup(request):
	userForm = UserForm(request.POST)
	profileForm = ProfileForm(request.POST)
	if (userForm.is_valid() and profileForm.is_valid()):
		user = userForm.save(commit=False)
		profile = profileForm.save(commit=False)
		username = userForm.cleaned_data['username']
		password = userForm.cleaned_data['password']
		user.set_password(password)
		user.save()
		profile.user = user
		profile.username = username
		profile.save()

		user = authenticate(username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('../')
		else:
			userForm = UserForm(None)
			profileForm = ProfileForm(None)
			return render(request, 'las/signinup.html', {'status': 'invalid', 'userform': userForm, 'profileform': profileForm})

def logout_view(request):
	logout(request)
	return render(request, 'las/logout_view.html')

def post_making(request):
	if request.method == "POST":
		editing = request.POST['editing']
		if (editing == 'aboutMe'):
			request.user.profile.aboutMe = request.POST['content']
			request.user.profile.save()
		elif (editing == 'jobDescription'):
			request.user.profile.jobDescription = request.POST['content']
			request.user.profile.save()
		elif (editing == 'new'):
			post = Post(poster=request.user.profile, content=request.POST['content'])
			post.save()
			editing = post.pk
		else:
			post = Post.objects.get(pk=editing)
			post.content = request.POST['content']
			post.save()
		return HttpResponse(editing)
	else:
		editing = request.GET['editing']
		if (editing == 'aboutMe'):
			content = request.user.profile.aboutMe
		elif (editing == 'jobDescription'):
			content = request.user.profile.jobDescription
		elif (editing == 'new'):
			content = None
		else:
			content = Post.objects.get(pk=editing).content
		return render(request, 'las/post_making.html', {'editing': editing, 'content': content})

def profile(request):
	edited = request.POST['edited'] if request.method == "POST" else None
	if (request.method == "POST"):
		poster = request.POST['poster']
	elif (request.GET.get('poster')):
		poster = request.GET.get('poster')
	else:
		poster = request.user.username

	poster = User.objects.get(username=poster)
	posts = Post.objects.filter(poster=poster.profile).order_by('-date')
	return render(request, 'las/profile.html', {'posts': posts, 'edited': edited, 'poster': poster})

class Posts(View):
	def get(self, request):
		post = Post.objects.get(pk=request.GET.get('id'))
		return HttpResponse(post.content)

	def post(self, request):
		post = Post.objects.get(pk=request.POST.get('deleting'))
		post.delete()
		posts = Post.objects.filter(poster=request.user.profile).order_by('-date')
		return render(request, 'las/profile.html', {'posts': posts, 'edited': 'deleted', 'poster': request.user})