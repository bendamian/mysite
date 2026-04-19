from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Contact
from django.db.models import Q
from blog.forms import ContactForm
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse

# Create your views here.

def index(request):
    form = ContactForm()
    contacts = request.user.contacts.all().order_by('-created_at') if request.user.is_authenticated else []
    context = {
        'contacts': contacts,
        'form': form
    }
    return render(request, 'index.html', context)


@login_required
def search_contacts(request):
    import time
    time.sleep(2)  # Simulate delay
    query = request.GET.get('search', '')
    contacts = request.user.contacts.filter(
        Q(name__icontains=query) | Q(email__icontains=query)
    ).order_by('-created_at') if request.user.is_authenticated else []

    context = {
        'contacts': contacts
    }
    return render(request, 'partials/contact-list.html', context)


@require_http_methods(["POST"])
@login_required
def add_contact(request):
    form = ContactForm(request.POST)
    form.instance.user = request.user  # ✅ important

    if form.is_valid():
        contact = form.save()

        response = render(request, 'partials/contact-row.html', {
            'contact': contact
        })
        response['HX-Trigger'] = 'success'
        return response

    return render(request, 'partials/add-contact-modal.html', {
        'form': form
    })
