# initiative/forms.py

from django import forms
from django.core.exceptions import ValidationError

from initiative.models import Initiative, Participant


EMPTY_PARTICIPANT_ERROR = "You can't have an empty initiative participant!"
DUPLICATE_PARTICIPANT_ERROR = "You've already got this in your initiative!"

class ParticipantForm(forms.models.ModelForm):

	class Meta:
		model = Participant
		fields = ('name',)
		widgets = {
			'name': forms.fields.TextInput(attrs={
				'placeholder': 'Enter a participant',
				'class': 'form-control input-lg',
			}),
		}
		error_messages = {
			'name': {'required': EMPTY_PARTICIPANT_ERROR}
		}
	
	
class NewInitiativeForm(ParticipantForm):
	
	def save(self, owner):
		if owner.is_authenticated:
			return Initiative.create_new(first_participant_text=self.cleaned_data['name'], owner=owner)
		else:
			return Initiative.create_new(first_participant_text=self.cleaned_data['name'])
	
		
class ExistingInitiativeParticipantForm(ParticipantForm):
	
	def __init__(self, for_initiative, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.instance.initiative = for_initiative
	
	def validate_unique(self):
		try:
			self.instance.validate_unique()
		except ValidationError as e:
			e.error_dict = {'name': [DUPLICATE_PARTICIPANT_ERROR]}
			self._update_errors(e)
	
	