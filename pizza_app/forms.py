from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Pizza, Size, Topping, Drink

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
        return user

class PizzaSelectionForm(forms.Form):
    pizza = forms.ModelChoiceField(
        queryset=Pizza.objects.filter(available=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label=None
    )
    
    size = forms.ModelChoiceField(
        queryset=Size.objects.all(),
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        empty_label=None
    )
    
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 5rem;'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # If initial pizza is provided, limit available toppings
        if 'initial' in kwargs and 'pizza' in kwargs['initial']:
            pizza_id = kwargs['initial']['pizza']
            pizza = Pizza.objects.get(id=pizza_id)
            self.available_toppings = pizza.available_toppings.filter(available=True)
        else:
            self.available_toppings = Topping.objects.filter(available=True)

class ToppingSelectionForm(forms.Form):
    def __init__(self, *args, available_toppings=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        if available_toppings:
            # Create a checkbox field for each available topping
            for topping in available_toppings:
                self.fields[f'topping_{topping.id}'] = forms.BooleanField(
                    label=f"{topping.name} (+${topping.small_price})",
                    required=False,
                    widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
                )

class DrinkSelectionForm(forms.Form):
    drink = forms.ModelChoiceField(
        queryset=Drink.objects.filter(available=True),
        widget=forms.Select(attrs={'class': 'form-select'}),
        empty_label=None
    )
    
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'style': 'width: 5rem;'})
    ) 