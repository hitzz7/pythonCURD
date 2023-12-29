from django.db import models
from django.core.exceptions import ValidationError
# Create your models here.

def validate_10_digits(value):
    if not value.isdigit() or len(value) != 10:
        raise ValidationError("Input must be a 10-digit number.")
    
class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=10,validators=[validate_10_digits])
    address = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    MALE = 1
    FEMALE = 0

    GENDER_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
    )

    gender = models.IntegerField(choices=GENDER_CHOICES,default=MALE) 
    def __str__(self):
        return str(self.name)
    

class Hobby(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user_hobby',null=True,blank=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name