from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Contact

# Create your views here.

def index(request):
    
    contacts = request.user.contacts.all().order_by('-created_at') if request.user.is_authenticated else []
    context = {
        'contacts': contacts
    }
    return render(request, 'index.html', context)
