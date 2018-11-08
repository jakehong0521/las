from django.urls import path
from django.conf.urls import url
from . import views
from las.views import Posts

urlpatterns = [
	path('', views.index, name='index'),
	path('category/', views.category, name='category'),
	path('guide/', views.guide, name='guide'),
	path('signinup/', views.signinup, name='signinup'),
	path('signin/', views.signin, name='signin'),
	path('signup/', views.signup, name='signup'),
	path('logout_view/', views.logout_view, name='logout_view'),
	path('post_making/', views.post_making, name='post_making'),
	path('profile/', views.profile, name='profile'),
	path('posts/', Posts.as_view(), name='posts'),
]