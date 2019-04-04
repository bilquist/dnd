# initiative/views.py

from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import redirect, render
from initiative.models import Initiative, Participant


# Create your views here.
def home_page(request):
	return render(request, 'initiative/home.html')

def view_initiative(request, initiative_id):
	initiative = Initiative.objects.get(id=initiative_id)
	error = None
	
	if request.method == 'POST':
		try:
			participant = Participant(name=request.POST['participant_text'], initiative=initiative)
			participant.full_clean()
			participant.save()
			return redirect(initiative)
		except ValidationError:
			error = "You can't have an empty initiative participant!"
	return render(request, 'initiative/initiative.html', {'initiative': initiative, 'error': error})
	
def new_initiative(request):
	initiative = Initiative.objects.create()
	participant = Participant(name=request.POST['participant_text'], initiative=initiative)
	try:
		participant.full_clean()
		participant.save()
	except ValidationError:
		initiative.delete()
		error = "You can't have an empty initiative participant!"
		return render(request, 'initiative/home.html', {'error': error})
	return redirect(initiative)

