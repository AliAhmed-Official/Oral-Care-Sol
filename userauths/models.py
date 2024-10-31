from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    User_Email = models.EmailField(unique=True)
    username = models.CharField(max_length=50)
    USERNAME_FIELD = 'User_Email'
    REQUIRED_FIELDS = ['username']
    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    image = models.ImageField(upload_to="image", blank = True)
    full_name = models.CharField(max_length = 50, null = True, blank = True)
    bio = models.CharField(max_length = 200, blank = True)
    phone = models.CharField(max_length=14, blank = True)
    verified = models.BooleanField(default = False)
    
    def __str__(self):
        return self.full_name