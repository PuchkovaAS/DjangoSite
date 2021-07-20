from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView

from .models import Profile


class MainView(TemplateView):
    template_name = "index.html"


def index(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    return render(request, "index.html")


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
    template_name = "user/user_edit.html"

    # View
    # def get(self, request, slug):
    #     user = Profile.objects.get(url=slug)
    #     return render(request, "user/user_edit.html", context={"user": user})
