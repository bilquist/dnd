# initiative/views.py

from django.shortcuts import redirect, render
from django.http import HttpResponse
from initiative.models import Participant


# Create your views here.
def home_page(request):
	if request.method == 'POST':
		Participant.objects.create(name=request.POST['participant_text'])
		return redirect('/')

	participants = Participant.objects.all()
	return render(request, 'initiative/home.html', {'participants': participants})

