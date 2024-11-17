from django.db import models
from django.contrib.auth.models import AbstractUser


def get_profile_pic_path(instance,file_name):
    return 'profiles/{0}/pic/{1}'.format(instance.email,file_name)
class User(AbstractUser):
    avatar=models.ImageField(upload_to=get_profile_pic_path,null=True,blank=True)

    @property
    def cover(self):
        if not self.avatar:
            return '/media/images/profiles/user-profile.png'
        return self.avatar.url
    @property
    def name(self):
        if not self.first_name:
            return self.username
        return self.first_name.capitalize()+" "+self.last_name.capitalize()

    def __str__(self):
        return self.name