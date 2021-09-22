from django import forms

from .models import Profile, UserStatistic, AgentProject


class UserLocAddForm(forms.ModelForm):
    # генерирует html формы
    # данный класс уже связан с моделью

    class Meta:
        model = UserStatistic
        fields = ['user_location', 'description', 'pub_date']
        widgets = {
            'user_location': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'pub_date': forms.DateInput(format='%Y-%m-%d'),
        }


class AgentEditForm(forms.ModelForm):
    # генерирует html формы
    # данный класс уже связан с моделью
    class Meta:
        model = AgentProject
        fields = ['position', 'description', 'location', 'phone_number', 'email']
        widgets = {
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(),
        }
