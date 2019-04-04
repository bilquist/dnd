# initiative/views.py

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect, render

from initiative.forms import EMPTY_PARTICIPANT_ERROR, ParticipantForm
from initiative.models import Initiative, Participant



# Create your views here.
def home_page(request):
	return render(request, 'initiative/home.html', {'form': ParticipantForm()})

def view_initiative(request, initiative_id):
	initiative = Initiative.objects.get(id=initiative_id)
	form = ParticipantForm()	
	if request.method == 'POST':
		form = ParticipantForm(data=request.POST)
		if form.is_valid():
			form.save(for_initiative=initiative)
			return redirect(initiative)
	return render(request, 'initiative/initiative.html', {'initiative': initiative, 'form': form})
	
def new_initiative(request):
	form = ParticipantForm(data=request.POST)
	if form.is_valid():
		initiative = Initiative.objects.create()
		Participant.objects.create(name=request.POST['name'], initiative=initiative)
		return redirect(initiative)
	else:
		return render(request, 'initiative/home.html', {'form': form})


