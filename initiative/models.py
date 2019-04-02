# initiative/models.py

from django.db import models

# Create your models here.
class Participant(models.Model):
	name = models.TextField()
	is_pc = models.BooleanField(default=False)