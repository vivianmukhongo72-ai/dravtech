from django import forms
from main.models import Product, ProductInquiry


class DemoRequestForm(forms.ModelForm):
    class Meta:
        model = ProductInquiry
        fields = ['name', 'email', 'company', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address',
                'required': True
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your company name',
                'required': False
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your phone number',
                'required': False
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tell us what you\'d like to see in the demo...',
                'rows': 5,
                'required': True
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Your Name'
        self.fields['email'].label = 'Email Address'
        self.fields['company'].label = 'Company / Organisation'
        self.fields['phone'].label = 'Phone / WhatsApp'
        self.fields['message'].label = 'What would you like to see in the demo?'
