from django import forms

from .models import UserStatistic, AgentProject, Project, Profile, HistoryProject


class UserLocAddForm(forms.ModelForm):
    # генерирует html формы
    # данный класс уже связан с моделью

    class Meta:
        model = UserStatistic
        fields = ['user_location', 'project', 'description', 'pub_date']
        widgets = {
            'user_location': forms.Select(attrs={'class': 'form-control'}),
            'project': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'pub_date': forms.DateInput(format='%Y-%m-%d'),

        }


class AgentEditForm(forms.ModelForm):
    # генерирует html формы
    # данный класс уже связан с моделью
    class Meta:
        model = AgentProject
        fields = ['position', 'organisation', 'description', 'location', 'phone_number', 'email']
        widgets = {
            'position': forms.TextInput(attrs={'class': 'form-control'}),
            'organisation': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.CheckboxSelectMultiple(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(),
        }


class ProjectEditForm(forms.ModelForm):
    # генерирует html формы
    # данный класс уже связан с моделью
    class Meta:
        model = Project
        fields = ['status', 'description', 'tasks']
        widgets = {
            'status': forms.RadioSelect(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'tasks': forms.Textarea(attrs={'class': 'form-control'}),
        }


class UserEditForm(forms.ModelForm):
    # генерирует html формы
    # данный класс уже связан с моделью
    class Meta:
        model = Profile
        fields = ['tabel_num', 'position', 'phone_number']
        widgets = {
            'tabel_num': forms.TextInput(attrs={'class': 'form-control p-2'}),
            'position': forms.TextInput(attrs={'class': 'form-control p-2'}),
            'phone_number': forms.Textarea(attrs={'class': 'form-control p-2'}),

        }


class HistoryAddForm(forms.ModelForm):
    # генерирует html формы
    # данный класс уже связан с моделью
    class Meta:
        model = HistoryProject
        fields = ['user_add', 'description', 'pub_date']
        widgets = {
            'user_add': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'pub_date': forms.DateInput(attrs={'class': 'form-control'}),
        }
