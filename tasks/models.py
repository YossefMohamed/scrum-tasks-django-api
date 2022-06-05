from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    pinned = models.BooleanField(default=False)
    assign = models.ForeignKey('User',related_name="assign" , on_delete=models.CASCADE , blank=True , null=True)
    creator = models.ForeignKey('User', related_name="creator" ,on_delete=models.CASCADE , blank=True , null=True)
    def __str__(self):
        return self.title
    # before saving
    def save(self, *args, **kwargs):
        self.assign = self.creator
        print(*args, **kwargs)
        super().save(*args, **kwargs)

        


class User (AbstractUser):
    id = models.TextField(primary_key = True,default = uuid.uuid4,editable = False)
    age             = models.IntegerField(default=18)
    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['age']
    def __str__(self):
        return self.username + f"{self.age}"
