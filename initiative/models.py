# initiative/models.py

from django.db import models

# Create your models here.
class Initiative(models.Model):
	pass
	

class Participant(models.Model):
	name = models.TextField()
	is_pc = models.BooleanField(default=False)
	initiative = models.ForeignKey(Initiative, on_delete=models.CASCADE, default=None)
	
	