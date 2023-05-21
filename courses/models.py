from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import UserManager
from django.utils.safestring import mark_safe

class Course(models.Model):
    name = models.CharField(max_length=100, null=False)
    price = models.IntegerField(null=False)
    discount = models.IntegerField(null=False, default=0)
    active = models.BooleanField(default=False)
    thumbnail = models.ImageField(upload_to='courses/')
    length = models.IntegerField(null=False)
    
    def __str__(self):
        return self.name
    

class CourseVideos(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=False)
    link = models.CharField(max_length=200, null=False)
    
    def __str__(self):
        return self.course.name
    

class CourseLearns(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False)
    
    def __str__(self):
        return self.course.name
    
    
class CourseRequirements(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=False)
    
    def __str__(self):
        return self.course.name
    

class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    
    name = models.CharField(max_length=150)
    email = models.EmailField('Email address', unique=True)
    username = models.CharField(max_length=50, unique=True)
    gender = models.CharField('Gender', max_length=1, choices=GENDER_CHOICES)
    dob = models.DateField('Date of birth', null=True)
    profile_image = models.ImageField('Profile image', upload_to='profiles/')
    address = models.CharField('Address', max_length=300)
    telephone_number = models.CharField('Telephone', max_length=20)
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def image(self):
        return mark_safe('<img src="%s" width=50px; height: 50px />' % (self.profile_image.url))
  
    def __str__(self):
        return self.email
    
    
class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return str(self.user)
    
    
class Shipment(models.Model):
    course_name = models.CharField(max_length=150)
    user_name = models.CharField(max_length=150)
    email = models.EmailField()
    address = models.CharField(max_length=300)
    telephone_number = models.CharField(max_length=20)
    course_price = models.FloatField()
    buy_date = models.DateTimeField(default=timezone.now)
    paid_status = models.CharField(max_length=20, default='unpaid')
    invoice = models.CharField(max_length=200)
    
    def __str__(self):
        return self.user_name
    
