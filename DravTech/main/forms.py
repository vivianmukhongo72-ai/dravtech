from django import forms
from django.utils import timezone

from .models import ProductInquiry, ContactMessage, Product



class ContactForm(forms.ModelForm):

    class Meta:
        model  = ContactMessage
        fields = ['name', 'email', 'phone', 'company', 'contact_type', 'priority', 'subject', 'message']

    # ── Validation ────────────────────────────────────────────────────────────

    def clean_name(self):
        name = self.cleaned_data.get('name', '').strip()
        if len(name) < 2:
            raise forms.ValidationError("Please enter your full name (at least 2 characters).")
        return name

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if phone:
            digits = ''.join(filter(str.isdigit, phone))
            if len(digits) < 7:
                raise forms.ValidationError("Please enter a valid phone number.")
        return phone

    def clean_subject(self):
        subject = self.cleaned_data.get('subject', '').strip()
        if len(subject) < 5:
            raise forms.ValidationError("Subject must be at least 5 characters.")
        return subject

    def clean_message(self):
        message = self.cleaned_data.get('message', '').strip()
        if len(message) < 20:
            raise forms.ValidationError("Please provide a bit more detail (at least 20 characters).")
        return message

class RequestDemoForm(forms.ModelForm):
    """Form backing the unified demo request flow."""
    
    # Available time slots for demo booking
    TIME_SLOT_CHOICES = [
        ('9am-10am', '9:00 AM - 10:00 AM'),
        ('10am-12pm', '10:00 AM - 12:00 PM'),
        ('1pm-3pm', '1:00 PM - 3:00 PM'),
        ('3pm-5pm', '3:00 PM - 5:00 PM'),
    ]
    
    product = forms.ModelChoiceField(
        queryset=Product.objects.filter(is_active=True, product_type='digital', requires_demo=True),
        empty_label="Select a product",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your full name',
            'required': True,
        })
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com',
            'required': True,
        })
    )
    
    company = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Company or organization (optional)',
        })
    )
    
    phone = forms.CharField(
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone or WhatsApp (optional)',
        })
    )
    
    preferred_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date',
            'min': (timezone.now() + timezone.timedelta(days=1)).strftime('%Y-%m-%d'),
        })
    )
    
    preferred_time = forms.ChoiceField(
        choices=TIME_SLOT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Tell us about your use case, timeline, and goals.',
            'required': True,
        })
    )

    class Meta:
        model = ProductInquiry
        fields = ['product', 'name', 'email', 'company', 'phone', 'preferred_date', 'preferred_time', 'message']
