# initiative/views.py

from django.shortcuts import render
from django.http import HttpResponse



# Create your views here.
def home_page(request):
	return render(request, 'initiative/home.html', {
		'new_participant_text': request.POST.get('participant_text', ''),
	})
