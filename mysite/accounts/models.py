from django.db import models
from django.urls import reverse_lazy
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password=password
        )
        user.is_staff = True
        user.is_admin = True
        user.save()
        return user


class User(AbstractUser):
    image = models.ImageField(blank=True)
    bio = models.TextField(blank=True)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_username(self):
        return self.username


class Project(models.Model):
    name = models.SlugField(max_length=255)
    description = models.TextField()
    timeline = models.CharField(max_length=255)
    requirements = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse_lazy('project:home', kwargs={'username': self.created_by, 'slug': self.name})


class Positions(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    accepted = models.BooleanField(blank=True, null=True)
    time = models.CharField(max_length=255)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    user  = models.ForeignKey(to=User, on_delete=models.CASCADE)


class Skill(models.Model):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class MyProject(models.Model):
    name = models.CharField(max_length=255)
    url = models.URLField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
