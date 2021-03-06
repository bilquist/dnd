# initiative/urls.py

"""dnd/initiative URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.urls import path
from initiative import views


urlpatterns = [
	path('new', views.new_initiative, name='new_initiative'),
	path('<int:initiative_id>/', views.view_initiative, name='view_initiative'),
	path('users/<str:email>/', views.my_initiatives, name='my_initiatives'),
]
