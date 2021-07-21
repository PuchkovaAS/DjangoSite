from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView, UpdateView

from .models import Profile


class MainView(TemplateView):
    template_name = "index.html"


def index(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    return render(request, "index.html")


class UsersTagView(ListView):
    model = Profile
    template_name = "user/users_list.html"

    def get_queryset(self):
        queryset = self.model.objects.filter(user_location=self.request.user_location)
        return queryset

class UsersView(ListView):
    model = Profile
    template_name = "user/users_list.html"
    queryset = Profile.objects.all()

    # View
    # def get(self, request):
    #     users = Profile.objects.all()
    #     return render(request, "user/users_list.html", context={'users': users})


class UserDetailView(DetailView):
    model = Profile
    slug_field = "url"
    template_name = "user/user_detail.html"

    # View
    # def get(self, request, slug):
    #     user = Profile.objects.get(url=slug)
    #     return render(request, "user/user_edit.html", context={"user": user})


class UserLocationAdd(UpdateView):
    model = Profile
    template_name = 'user/user_edit.html'
    # form_class = UserLocAddForm
    success_url = reverse_lazy('user_list')
    slug_field = "url"
    # queryset = Profile.objects.filter(url=slug_field)
    fields = ['user_location', 'description', 'pub_date']
