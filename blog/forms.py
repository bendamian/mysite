from django import forms
from blog.models import Contact
from django.core.exceptions import ValidationError


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email']
        
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'peer w-full input input-bordered px-4 pt-5 pb-2  focus:ring-2 focus:ring-blue-200',
                
            }),
            'email': forms.EmailInput(attrs={
                'class': 'peer w-full input input-bordered px-4 pt-5 pb-2 focus:ring-2 focus:ring-blue-200',
                
            }),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        user = self.instance.user if self.instance.user else self.initial.get(
            'user')

        if Contact.objects.filter(user=user, email=email).exists():
            raise ValidationError(
                "This email already exists in your contacts.")

        return email
