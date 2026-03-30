from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Contact
from django.db.models import Q

# Create your views here.

def index(request):
    
    contacts = request.user.contacts.all().order_by('-created_at') if request.user.is_authenticated else []
    context = {
        'contacts': contacts
    }
    return render(request, 'index.html', context)


def search_contacts(request):
    query = request.GET.get('search', '')
    contacts = request.user.contacts.filter(
        Q(name__icontains=query) | Q(email__icontains=query)
    ).order_by('-created_at') if request.user.is_authenticated else []

    context = {
        'contacts': contacts
    }
    return render(request, 'partials/contact-list.html', context)
