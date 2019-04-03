# initiative/views.py

from django.shortcuts import redirect, render
from django.http import HttpResponse
from initiative.models import Initiative, Participant


# Create your views here.
def home_page(request):
	return render(request, 'initiative/home.html')

def initiative_list(request, initiative_id):
	initiative = Initiative.objects.get(id=initiative_id)
	return render(request, 'initiative/initiative.html', {'initiative': initiative})
	
def new_initiative(request):
	initiative = Initiative.objects.create()
	Participant.objects.create(name=request.POST['participant_text'], initiative=initiative)
	return redirect(f'/initiative/{initiative.id}/')

def add_participant(request, initiative_id):
	initiative = Initiative.objects.get(id=initiative_id)
	Participant.objects.create(name=request.POST['participant_text'], initiative=initiative)
	return redirect(f'/initiative/{initiative.id}/')