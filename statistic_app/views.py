from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, DetailView, ListView, UpdateView

from .models import Profile, UserLocation, UserStatistic


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
        queryset = Profile.objects.filter(user_location__in=filter_data)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(UsersFilterView, self).get_context_data(**kwargs)
        context['location'] = UserLocation.objects.all()
        context['filter_id'] = self.filter_id
        return context


class UsersView(ListView):
    model = Profile
    template_name = "user/users_list.html"

    paginate_by = 60

    def get_queryset(self):
        search_quary = self.request.GET.get('search_line', '')
        if search_quary:
            queryset = Profile.objects.filter(
                Q(user__icontains=search_quary) | Q(father_name__icontains=search_quary) | Q(
                    position__icontains=search_quary))
        else:
            queryset = Profile.objects.all()
        return queryset

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

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        context['statistics'] = UserStatistic.objects.filter(user_name=self.object).order_by('-pk')
        context['statistic'] = context['statistics'][0]
        return context

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

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        request.POST = request.POST.copy()
        new_obj = UserStatistic.objects.create(user_name=self.object,
                                               user_location=UserLocation.objects.get(
                                                   pk=int(request.POST['user_location'])),
                                               description=request.POST['description'])
        new_obj.save()
        return super(UserLocationAdd, self).post(request, **kwargs)
