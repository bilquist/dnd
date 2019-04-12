# initiative/models.py

from django.conf import settings
from django.db import models
from django.urls import reverse



# Create your models here.
class Initiative(models.Model):
	
	owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
	
	def get_absolute_url(self):
		return reverse('view_initiative', args=[self.id])
	
	@property
	def name(self):
		return self.participant_set.first().name
	
	@staticmethod
	def create_new(first_participant_text, owner=None):
		initiative = Initiative.objects.create(owner=owner)
		Participant.objects.create(name=first_participant_text, initiative=initiative)
		return initiative


class Participant(models.Model):
	name = models.TextField()
	is_pc = models.BooleanField(default=False)
	initiative = models.ForeignKey(Initiative, on_delete=models.CASCADE, default=None)
	
	class Meta:
		ordering = ('id',)
		unique_together = ('initiative', 'name')
	
	def __str__(self):
		return self.name
	