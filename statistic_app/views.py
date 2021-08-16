import operator
from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, View

from .models import Profile, UserLocation, UserStatistic
from .my_data import PersonData

from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


class MainView(LoginRequiredMixin, TemplateView):
    login_url = '/accounts/login'
    template_name = "index.html"


def index(request):
    if not request.user.is_authenticated:
        return redirect('/accounts/login')
    return render(request, "index.html")


class UsersFilterView(LoginRequiredMixin, ListView):
    login_url = '/accounts/login'
    template_name = "user/users_list.html"
    paginate_by = 60

    def get_queryset(self):
        filter_data = self.request.GET.getlist("check_location")
        self.filter_id = [int(data) for data in filter_data]
        queryset = Profile.objects.filter(user_location__in=filter_data)
        # ordered = sorted(queryset, key=operator.attrgetter('user.username'))
        # print(ordered)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(UsersFilterView, self).get_context_data(**kwargs)
        context['location'] = UserLocation.objects.all()
        context['filter_id'] = self.filter_id
        return context


class UsersView(LoginRequiredMixin, View):
    login_url = '/accounts/login'
    model = Profile
    template_name = "user/users_list.html"
    paginate_by = 60
    search_quary = ''

    def post(self, request):
        self.search_quary = request.POST.get('search_line')
        contex = self.get_context_data()
        return render(request, self.template_name, contex)

    def get(self, request):
        contex = self.get_context_data()
        return render(request, self.template_name, contex)

    def get_queryset(self):
        if self.search_quary:
            queryset = Profile.objects.filter(Q(user__last_name__icontains=self.search_quary) |
                                              Q(user__first_name__icontains=self.search_quary) |
                                              Q(father_name__icontains=self.search_quary) | Q(
                position__icontains=self.search_quary))
        else:
            queryset = Profile.objects.all()

        ordered = sorted(queryset, key=operator.attrgetter('user.username'))
        return ordered

    def get_context_data(self):
        context = {}
        context['profile_list'] = self.get_queryset()
        context['location'] = UserLocation.objects.all()
        context['filter_id'] = list(range(1, len(context['location']) + 1))
        return context


class UserStatistics(LoginRequiredMixin, View):
    login_url = '/accounts/login'
    model = Profile
    template_name = "user/statistics.html"
    paginate_by = 60
    search_quary = ''
    delta = 28
    WEEKDAYS = {
        1: 'Пн',
        2: 'Вт',
        3: 'Ср',
        4: 'Чт',
        5: 'Пт',
        6: 'Сб',
        7: 'Вс'
    }


    def get_statistics(self, users):
        user_statistics = {}
        for user in users:
            # data = UserStatistic.objects.filter(
            #     pub_date__range=[(datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
            #                      datetime.now().strftime("%Y-%m-%d")], user_name=user)
            data_DB = UserStatistic.objects.filter(user_name=user).order_by('pub_date')
            new_user_stat = PersonData(data=data_DB, date_time=self.date_time)
            result = new_user_stat.get_calendar()
            user_statistics.update({user.user.username: result})
            # for d in data:
            #     print(user, d.user_location, d.pub_date, sep='\t', end='\n')
            # print(user_statistics[user])
        return user_statistics

    def get_date_time(self, current_time):
        end = datetime.now() - timedelta(days=self.delta * (current_time - 1))
        start = end - timedelta(days=self.delta)

        date_generated = [start + timedelta(days=x) for x in range(1, (end - start).days + 1)]
        return list(reversed([date.date() for date in date_generated]))

    def get(self, request):
        self.page_number = request.GET.get("page", 1)
        self.date_time = self.get_date_time(int(self.page_number))
        context = {}
        profiles = Profile.objects.all()
        ordered = sorted(profiles, key=operator.attrgetter('user.username'))
        
        context['profile_list'] = ordered
        context['user_statistics'] = self.get_statistics(context['profile_list'])
        context['location'] = UserLocation.objects.all()
        context['filter_id'] = list(range(1, len(context['location']) + 1))
        context["date_time"] = [{'weekday': self.WEEKDAYS[day.isoweekday()], 'day': day.strftime("%d.%m.%y")} for day in self.date_time]
        context["prev_url"] = f'?page={int(self.page_number) - 1}' if int(self.page_number) > 1 else ''
        context["next_url"] = f'?page={int(self.page_number) + 1}'
        # print(context['user_statistics'])
        return render(request, self.template_name, context=context)


# class UsersView(ListView):
#     model = Profile
#     template_name = "user/users_list.html"
#
#     paginate_by = 60
#
#
#     def get_queryset(self):
#         search_quary = self.request.GET.get('search_line', '')
#         if search_quary:
#             queryset = Profile.objects.filter(
#                 Q(user__icontains=search_quary) | Q(father_name__icontains=search_quary) | Q(
#                     position__icontains=search_quary))
#         else:
#             queryset = Profile.objects.all()
#         return queryset
#
#     def get_context_data(self, **kwargs):
#         context = super(UsersView, self).get_context_data(**kwargs)
#         context['location'] = UserLocation.objects.all()
#         context['filter_id'] = list(range(1, len(context['location']) + 1))
#         return context

# View
# def get(self, request):
#     users = Profile.objects.all()
#     return render(request, "user/users_list.html", context={'users': users})


# class UserDetailView(DetailView):
#     model = Profile
#     slug_field = "url"
#     template_name = "user/user_detail.html"
#
#     def get_context_data(self, **kwargs):
#         context = super(UserDetailView, self).get_context_data(**kwargs)
#         context['statistics'] = UserStatistic.objects.filter(user_name=self.object).order_by('-pk')
#         context['statistic'] = context['statistics'][0]
#         return context

class UserDetailView(LoginRequiredMixin, View):
    login_url = '/accounts/login'
    model = Profile
    slug_field = "url"
    template_name = "user/user_detail.html"
    pagination = 10

    def post(self, request, slug):
        self.pagination = int(request.POST.get('pagination'))
        contex = self.get_context_data(slug)
        return render(request, self.template_name, contex)

    def get(self, request, slug):
        contex = self.get_context_data(slug)

        return render(request, self.template_name, contex)

    def get_context_data(self, slug):
        context = {}
        object = get_object_or_404(self.model, url__iexact=slug)
        context['profile'] = get_object_or_404(self.model, url__iexact=slug)
        context['statistics'] = UserStatistic.objects.filter(user_name=object).order_by('-pk')[:self.pagination]
        if context['statistics']:
            context['statistic'] = context['statistics'][0]
        context['pagination'] = self.pagination
        return context

    # View
    # def get(self, request, slug):
    #     user = Profile.objects.get(url=slug)
    #     return render(request, "user/user_edit.html", context={"user": user})


class UserLocationAdd(LoginRequiredMixin, UpdateView):
    login_url = '/accounts/login'
    model = Profile
    template_name = 'user/user_edit.html'
    # form_class = UserLocAddForm
    success_url = reverse_lazy('user_list')
    slug_field = "url"
    # queryset = Profile.objects.filter(url=slug_field)
    fields = ['user_location', 'description']

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        request.POST = request.POST.copy()
        new_obj = UserStatistic.objects.create(user_name=self.object,
                                               user_location=UserLocation.objects.get(
                                                   pk=int(request.POST['user_location'])),
                                               description=request.POST['description'])
        new_obj.save()
        return super(UserLocationAdd, self).post(request, **kwargs)
