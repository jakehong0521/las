from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	username = models.TextField(blank=True)
	title = models.CharField(max_length=40)
	company = models.CharField(max_length=40, blank=True)
	aboutMe = models.TextField(blank=True)
	jobDescription = models.TextField(blank=True)
	field = models.TextField(choices=(
		('N/A', 'N/A'),
    	('administration', 'Administration'),
    	('banking', 'Banking'),
	    ('design', 'Design'),
	    ('education', 'Education'),
	    ('engineering', 'Engineering'),
	    ('entrepreneur', 'Entrepreneur'),
	    ('government', 'Government'),
	    ('health', 'Health'),
	    ('legal', 'Legal'),
	    ('media', 'Media'),
	    ('research', 'Research'),
	    ('sales', 'Sales')
	), default='N/A')

	def __str__(self):
		return self.user.username + ' is ' + self.title

class Post(models.Model):
	date = models.DateField(default=datetime.date.today())
	poster = models.ForeignKey(Profile, on_delete=models.CASCADE)
	content = models.TextField(blank=True)