# orders/forms.py

from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['orderer_name', 'quantity', 'delivery_date', 'has_changes', 'note']
        
        widgets = {
            'delivery_date': forms.DateInput(attrs={'type': 'date'}),
            'note': forms.Textarea(attrs={'rows': 3, 'placeholder': '変更点などがあればご記入ください'}),
        }
        labels = {
            'has_changes': '前回からの変更はありますか？',
        }