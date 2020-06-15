from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse



class PublishedManager(models.Manager):
	def get_queryset(self):
		return super(PublishedManager,self).get_queryset().filter(status='published')
""" 
		this anther manager but this wn dont need ordering meta

class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        # Post.objects.all() = super(PostManager, self).all()
        return super(PostManager, self).filter(status='published').filter(publish__lte=timezone.now())
"""
class Post(models.Model):
	STATUS_CHOICES = (
		('draft', 'Draft'),
		('published', 'Published'),
	)
	title = models.CharField(max_length=250)
	slug = models.SlugField(max_length=250,
							unique_for_date='date_posted')
	author = models.ForeignKey(User,
								on_delete=models.CASCADE,
								related_name='blog_posts')
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	status = models.CharField(max_length=10,
								choices=STATUS_CHOICES,
								default='draft')
	

	class Meta:
		ordering = ('-date_posted',)								
	
	def __str__(self):
		return self.title
    
	def get_absolute_url(self):
 		return reverse('post-detail', args=[self.date_posted.year,
 												self.date_posted.month,
 												self.date_posted.day,
 												self.slug])
	'''this onws postmanger active
		
	objects = PostManager()
	
	'''

	objects = models.Manager() # The default manager.
	published = PublishedManager() # Our custom manager.
