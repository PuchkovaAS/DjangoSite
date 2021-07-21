from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView, UpdateView

from .models import Profile, UserLocation


class MainView(TemplateView):
    template_name = "index.html"


def index(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    return render(request, "index.html")


class UsersFilterView(ListView):
    template_name = "user/users_list.html"
    paginate_by = 60

    def get_queryset(self):
        filter_data = self.request.GET.getlist("check_location")
        self.filter_id = [int(data) for data in filter_data]
        queryset = Profile.objects.filter(pk__in=[int(data) - 1 for data in filter_data])
        return queryset

    def get_context_data(self, **kwargs):
        context = super(UsersFilterView, self).get_context_data(**kwargs)
        context['location'] = UserLocation.objects.all()
        context['filter_id'] = self.filter_id
        return context


class UsersView(ListView):
    model = Profile
    template_name = "user/users_list.html"
    queryset = Profile.objects.all()
    paginate_by = 60

    def get_context_data(self, **kwargs):
        context = super(UsersView, self).get_context_data(**kwargs)
        context['location'] = UserLocation.objects.all()
        context['filter_id'] = list(range(1, len(context['location']) + 1))
        return context

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
