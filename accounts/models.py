from django.db import models
from PIL import Image

from django.contrib.auth.models import User


class UserProfile(models.Model):

	role_select = (
        ('SuperAdmin','Super admin'),
        ('Admin','Admin'),
        ('Teacher','Teacher'),
        ('Student','Student'),    
    )

	"""User Table"""
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	fullName = models.CharField(max_length=50, default="")
	user_type = models.CharField(max_length=10, choices=role_select, default='TH')
	mobile_no = models.BigIntegerField(blank=True, null=True)
	image = models.ImageField(default='default.jpg',upload_to ='profile_pics', blank=True, null=True)
	emp_id = models.BigIntegerField(default=0, blank=True, null=True)
	addmission_number = models.BigIntegerField(default=0, blank=True, null=True)
	password = models.CharField(max_length=300)
	is_active = models.BooleanField(default=True)

	def __str__(self):
		return f"{self.user}"

	def save(self, *args, **kwargs):
		super(UserProfile, self).save(*args, **kwargs)
		try:
			img = Image.open(self.image.path)  # Open image using self
			if img.height > 300 or img.width > 300:
				new_img = (300, 300)
				img.thumbnail(new_img)
				img.save(self.image.path)
		except:
			pass