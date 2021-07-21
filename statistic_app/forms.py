from django import forms

from .models import Profile


class UserLocAddForm(forms.ModelForm):
    # генерирует html формы
    # данный класс уже связан с моделью

    class Meta:
        model = Profile
        fields = ['user_location']
        widgets = {
            'user_location': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'pub_date': forms.TextInput(attrs={'class': 'form-control'}),
        }

