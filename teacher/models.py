from django.db import models
from django.contrib.auth.models import User

class Teacher(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/Teacher/',null=True,blank=True)
    mobile = models.CharField(max_length=20,null=False)
    specialite = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_instance(self):
        return self
    def __str__(self):
        return self.user.first_name