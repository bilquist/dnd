# initiative/forms.py

from django import forms

from initiative.models import Participant


EMPTY_PARTICIPANT_ERROR = "You can't have an empty initiative participant!"

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
	