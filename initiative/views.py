# initiative/views.py

from django.shortcuts import redirect, render
from django.http import HttpResponse
from initiative.models import Initiative, Participant


# Create your views here.
def home_page(request):
	return render(request, 'initiative/home.html')

def initiative_list(request):
	participants = Participant.objects.all()
	return render(request, 'initiative/initiative.html', {'participants': participants})

def new_initiative(request):
	initiative = Initiative.objects.create()
	Participant.objects.create(name=request.POST['participant_text'], initiative=initiative)
	return redirect('/initiative/the-only-list-in-the-world/')