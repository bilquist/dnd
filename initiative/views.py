# initiative/views.py

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from initiative.models import Initiative, Participant


# Create your views here.
def home_page(request):
	return render(request, 'initiative/home.html')

def initiative_list(request, initiative_id):
	initiative = Initiative.objects.get(id=initiative_id)
	return render(request, 'initiative/initiative.html', {'initiative': initiative})
	
def new_initiative(request):
	initiative = Initiative.objects.create()
	participant = Participant(name=request.POST['participant_text'], initiative=initiative)
	try:
		participant.full_clean()
		participant.save()
	except ValidationError:
		initiative.delete()
		error = "You can't have an empty list item!"
		return render(request, 'initiative/home.html', {'error': error})
	return redirect(f'/initiative/{initiative.id}/')

def add_participant(request, initiative_id):
	initiative = Initiative.objects.get(id=initiative_id)
	Participant.objects.create(name=request.POST['participant_text'], initiative=initiative)
	return redirect(f'/initiative/{initiative.id}/')