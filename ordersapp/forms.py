from django import forms
from .models import Order, OrderItem


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('user',)


class OrderItemForm(forms.ModelForm):
    price = forms.CharField(label='Price', required=False)
    class Meta:
        model = OrderItem
        fields = '__all__'
