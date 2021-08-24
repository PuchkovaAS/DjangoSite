from django import forms

from .models import Profile, UserStatistic


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

