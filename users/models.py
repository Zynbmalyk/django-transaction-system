from django.db import models

# Create your models here.

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    user_code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.name