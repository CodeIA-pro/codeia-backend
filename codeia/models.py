from djongo import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        if not email: # If email is not provided 
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields) # Normalize email
        user.set_password(password) # Set password
        user.save(using=self._db) # Save user
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password)
        user.role = 'admin'
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db) # ._db meaning the database that is being used
        return user

class TypeComment(models.Model):
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    user = models.IntegerField(blank=False)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    type_comment = models.IntegerField(blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

class FAQ(models.Model):
    question = models.CharField(max_length=100, blank=True)
    answer = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Asset(models.Model):
    version = models.CharField(max_length=10, default='1.0.0', blank=True)
    titulo = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    more_description = models.TextField(blank=True)
    depth = models.IntegerField(default=0, blank=True)
    url = models.TextField(blank=True)
    is_father = models.BooleanField(default=False, blank=True)
    father_id = models.IntegerField(blank=False)
    project_id = models.IntegerField(blank=True)
    subsection = models.ArrayReferenceField(to='self', default=list, blank=True)

class Project(models.Model):
    title = models.CharField(max_length=100, blank=True)
    branch = models.CharField(max_length=100, blank=True)
    url_repo = models.TextField(blank=True)
    user_repo = models.TextField(blank=True)
    latest_build = models.DateTimeField(auto_now_add=True)
    last_version = models.CharField(max_length=100, blank=True)
    assets = models.ArrayReferenceField(to=Asset, default=list, blank=True)

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, unique=True)
    nationality = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True)
    projects = models.ArrayReferenceField(to=Project, default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=20, default='guest')
    objects = UserManager()

    USERNAME_FIELD = 'email' # This is the field that will be used to login