from django.db import models

# Create your models here.

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if postData['password'] != postData['password_confirmation']:
            errors['password_match'] = "Passwords do not match"
        if len(postData['password']) < 8:
            errors['len_password'] = "Password should be a least 8 characters"
        return errors

class User(models.Model):
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=100)
    birth_date = models.DateTimeField()
    objects = UserManager()

class Poke(models.Model):
    origin_user = models.ForeignKey(User, related_name="pokers", on_delete=models.CASCADE)
    destination_user = models.ForeignKey(User, related_name="pokes", on_delete=models.CASCADE)

