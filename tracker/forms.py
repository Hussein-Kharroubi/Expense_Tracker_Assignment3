from django.forms import ModelForm
from django import forms
from .models import Expense

class ExpenseForm(ModelForm):
	class Meta:
		model = Expense
		fields = ['category', 'store', 'amount', 'date', 'description']
		widgets = {'date': forms.DateInput(attrs={'type': 'date'})}



