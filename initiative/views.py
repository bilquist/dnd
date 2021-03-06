# initiative/views.py

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect, render

from initiative.forms import ExistingInitiativeParticipantForm, ParticipantForm, NewInitiativeForm
from initiative.models import Initiative, Participant



User = get_user_model()

# Create your views here.
def home_page(request):
	return render(request, 'initiative/home.html', {'form': ParticipantForm()})

def view_initiative(request, initiative_id):
	initiative = Initiative.objects.get(id=initiative_id)
	form = ExistingInitiativeParticipantForm(for_initiative=initiative)
	if request.method == 'POST':
		form = ExistingInitiativeParticipantForm(for_initiative=initiative, data=request.POST)
		if form.is_valid():
			form.save()
			return redirect(initiative)
	return render(request, 'initiative/initiative.html', {'initiative': initiative, 'form': form})
	
def new_initiative(request):
	form = NewInitiativeForm(data=request.POST)
	if form.is_valid():
		initiative = form.save(owner=request.user)
		return redirect(str(initiative.get_absolute_url()))
	return render(request, 'initiative/home.html', {'form': form})


def my_initiatives(request, email):
	owner = User.objects.get(email=email)
	return render(request, 'initiative/my_initiatives.html', {'owner': owner})
	