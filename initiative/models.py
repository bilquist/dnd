# initiative/models.py

from django.urls import reverse
from django.db import models



# Create your models here.
class Initiative(models.Model):
	
	def get_absolute_url(self):
		return reverse('view_initiative', args=[self.id])
	

class Participant(models.Model):
	name = models.TextField()
	is_pc = models.BooleanField(default=False)
	initiative = models.ForeignKey(Initiative, on_delete=models.CASCADE, default=None)
	
	