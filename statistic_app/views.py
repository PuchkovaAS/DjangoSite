import operator
from datetime import datetime, timedelta

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.template.defaulttags import register
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, View

from .forms import UserLocAddForm, AgentEditForm, ProjectEditForm, UserEditForm, HistoryAddForm
from .models import Profile, UserLocation, UserStatistic, Project, AgentProject, HistoryProject
from .my_data import PersonData
from .utils import ObjectUpdateMixin


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
    filter_id = []

    def get_queryset(self):
        filter_data = self.request.GET.getlist("check_location")
        self.filter_id = [int(data) for data in filter_data]
        queryset = Profile.objects.filter(user_location__in=filter_data)
        # ordered = sorted(queryset, key=operator.attrgetter('user.username'))
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
        return queryset

    def get_context_data(self):
        context = {}
        context['profile_list'] = self.get_queryset()
        context['location'] = UserLocation.objects.all()
        context['search_line'] = True
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

    def get_date_time(self, current_time, certain_time=None):
        if certain_time:
            end = datetime.strptime(certain_time, '%Y-%m-%d')
        else:
            end = datetime.now() - timedelta(days=self.delta * (current_time - 1))
        start = end - timedelta(days=self.delta)

        date_generated = [start + timedelta(days=x) for x in range(1, (end - start).days + 1)]
        return list(reversed([date.date() for date in date_generated]))

    def get(self, request):
        page_number = request.GET.get("page", 1)
        self.date_time = self.get_date_time(current_time=int(page_number),
                                            certain_time=request.GET.get('date', None))
        context = {}
        profiles = Profile.objects.all()
        ordered = sorted(profiles, key=operator.attrgetter('user.username'))

        context['profile_list'] = ordered
        context['user_statistics'] = self.get_statistics(context['profile_list'])
        context['location'] = UserLocation.objects.all()
        context['filter_id'] = list(range(1, len(context['location']) + 1))
        context["date_time"] = [{'weekday': self.WEEKDAYS[day.isoweekday()], 'day': day.strftime("%d.%m.%y")} for day in
                                self.date_time]
        context["prev_url"] = f'?page={int(page_number) - 1}' if int(page_number) > 1 else ''
        context["next_url"] = f'?page={int(page_number) + 1}'

        # context["date_url"] = request.GET.get("date", 1)

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

    def get_pagination(self, model, request, page_name, count_pagination=10):
        history_all = model.all()
        paginator = Paginator(history_all, count_pagination)
        page_number = request.GET.get(page_name, 1)

        result_data = paginator.get_page(page_number)

        is_paginated = result_data.has_other_pages()
        if result_data.has_previous():
            prev_url = f'?{page_name}={result_data.previous_page_number()}'
        else:
            prev_url = ''

        if result_data.has_next():
            next_url = f'?{page_name}={result_data.next_page_number()}'
        else:
            next_url = ''
        return result_data, is_paginated, prev_url, next_url

    def post(self, request, slug):
        contex = self.get_context_data(request, slug)
        return render(request, self.template_name, contex)

    def get(self, request, slug):

        contex = self.get_context_data(request, slug)

        return render(request, self.template_name, contex)

    def get_context_data(self, request, slug):
        context = {}
        object = get_object_or_404(self.model, url__iexact=slug)
        context['profile'] = get_object_or_404(self.model, url__iexact=slug)
        # context['statistics'] = UserStatistic.objects.filter(user_name=object)[:self.pagination]
        history, h_is_paginated, h_prev_url, h_next_url = self.get_pagination(
            model=UserStatistic.objects.filter(user_name=object), request=request,
            page_name='page', count_pagination=10)

        context['statistics'] = history
        context['prev_url'] = h_prev_url
        context['next_url'] = h_next_url
        context['is_paginated'] = h_is_paginated

        return context

    # View
    # def get(self, request, slug):
    #     user = Profile.objects.get(url=slug)
    #     return render(request, "user/user_edit.html", context={"user": user})


class UserLocationAdd(LoginRequiredMixin, View):
    form_model = UserLocAddForm
    login_url = '/accounts/login'
    model = UserStatistic
    template = 'user/user_add.html'
    success_url = reverse_lazy('user_list')
    fields = ['user_location', 'project', 'description', 'pub_date']

    def get(self, request, slug):
        profile = Profile.objects.get(url=slug)
        form = self.form_model()
        return render(request=request, template_name=self.template, context={'form': form, 'profile': profile})

    def post(self, request, slug):
        # prof_slug = request.build_absolute_uri().split('/')[-3]
        bound_form = self.form_model(request.POST)
        if bound_form.is_valid():
            profile = Profile.objects.get(url=slug)
            request.POST = request.POST.copy()
            location = UserLocation.objects.get(
                pk=int(request.POST['user_location']))
            new_obj = UserStatistic.objects.create(user_name=profile,
                                                   user_location=location,
                                                   description=request.POST['description'],
                                                   pub_date=request.POST['pub_date'],
                                                   project=Project.objects.get(pk=int(request.POST['project'])) if
                                                   request.POST['project'] else None)
            new_obj.save()

            last_statis = UserStatistic.objects.filter(user_name=profile)[0]
            profile.user_location = last_statis.user_location
            profile.project = last_statis.project
            profile.pub_date = last_statis.pub_date
            profile.description = last_statis.description
            profile.save()

            # profile.user_location = UserStatistic.objects.filter(user_name=profile).order_by('-pub_date')[:1][0]
            # profile.save()
            return redirect(self.success_url)
        else:
            return render(request, self.template, context={'form': bound_form})


# class UserLocationAdd(LoginRequiredMixin, UpdateView):
#     login_url = '/accounts/login'
#     model = Profile
#     template_name = 'user/user_edit.html'
#     # form_class = UserLocAddForm
#     success_url = reverse_lazy('user_list')
#     slug_field = "url"
#     # queryset = Profile.objects.filter(url=slug_field)
#     fields = ['user_location', 'description']
#
#     def post(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         request.POST = request.POST.copy()
#         new_obj = UserStatistic.objects.create(user_name=self.object,
#                                                user_location=UserLocation.objects.get(
#                                                    pk=int(request.POST['user_location'])),
#                                                description=request.POST['description'])
#         new_obj.save()
#         return super(UserLocationAdd, self).post(request, **kwargs)
class ProjectsView(LoginRequiredMixin, View):
    login_url = '/accounts/login'
    model = Project
    template_name = "project/project_list.html"
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
            queryset = self.model.objects.filter(Q(name__icontains=self.search_quary))
        else:
            queryset = self.model.objects.all()
        return queryset

    def get_context_data(self):
        context = {}
        context['project_list'] = self.get_queryset()
        context['search_line'] = True
        return context


class ProjectDetailView(LoginRequiredMixin, View):
    login_url = '/accounts/login'
    model = Project
    slug_field = "url"
    template_name = "project/project_detail.html"
    pagination = 10

    def get_pagination(self, model, request, page_name, count_pagination=3):
        history_all = model.all()
        paginator = Paginator(history_all, count_pagination)
        # http://127.0.0.1:8000/blog/?page=2
        page_number = request.GET.get(page_name, 1)

        result_data = paginator.get_page(page_number)

        is_paginated = result_data.has_other_pages()
        if result_data.has_previous():
            prev_url = f'?{page_name}={result_data.previous_page_number()}'
        else:
            prev_url = ''

        if result_data.has_next():
            next_url = f'?{page_name}={result_data.next_page_number()}'
        else:
            next_url = ''
        return result_data, is_paginated, prev_url, next_url

    def get_current_staff(self, object):
        result_staff = []
        all_staff = Profile.objects.all()
        for staff in all_staff:
            current_obj = UserStatistic.objects.filter(user_name=staff)[:1][0]
            if current_obj.project == object:
                result_staff.append(staff)
        return result_staff

    def post(self, request, slug):
        self.pagination = int(request.POST.get('pagination'))
        contex = self.get_context_data(slug)
        return render(request, self.template_name, contex)

    def get(self, request, slug):
        contex = self.get_context_data(request, slug)

        return render(request, self.template_name, contex)

    def get_context_data(self, request, slug):
        object = get_object_or_404(self.model, url__iexact=slug)

        # context['staff'] = get_object_or_404(AgentProject, location=object.id)

        history, h_is_paginated, h_prev_url, h_next_url = self.get_pagination(model=object.history, request=request,
                                                                              page_name='page', count_pagination=10)
        staff_history, s_is_paginated, s_prev_url, s_next_url = self.get_pagination(model=object.user, request=request,
                                                                                    page_name='page',
                                                                                    count_pagination=20)

        current_staff = self.get_current_staff(object)
        context = {'history': history,
                   'prev_url': h_prev_url,
                   'next_url': h_next_url,
                   'is_paginated': h_is_paginated,
                   'staff': staff_history,
                   's_prev_url': s_prev_url,
                   's_next_url': s_next_url,
                   's_is_paginated': s_is_paginated,
                   'project': object,
                   'current_staff': current_staff,
                   'location':UserLocation.objects.all()
                   }

        return context


class AgentView(LoginRequiredMixin, View):
    login_url = '/accounts/login'
    model = Profile
    template_name = "agent/agent_list.html"
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
            queryset = AgentProject.objects.filter(Q(last_name__icontains=self.search_quary) |
                                                   Q(first_name__icontains=self.search_quary) |
                                                   Q(father_name__icontains=self.search_quary) |
                                                   Q(position__icontains=self.search_quary) |
                                                   Q(organisation__icontains=self.search_quary))
        else:
            queryset = AgentProject.objects.all()
        return queryset

    def get_context_data(self):
        context = {}
        context['agent_list'] = self.get_queryset()
        context['search_line'] = True
        return context


class AgentDetailView(LoginRequiredMixin, View):
    login_url = '/accounts/login'
    model = AgentProject
    slug_field = "url"
    template_name = "agent/agent_detail.html"
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
        context['agent'] = get_object_or_404(self.model, url__iexact=slug)
        return context

    # View
    # def get(self, request, slug):
    #     user = Profile.objects.get(url=slug)
    #     return render(request, "user/user_edit.html", context={"user": user})


class AgentEditView(LoginRequiredMixin, ObjectUpdateMixin, View):
    form_model = AgentEditForm
    login_url = '/accounts/login'
    model = AgentProject
    template = 'agent/agent_edit.html'
    success_url = reverse_lazy('agent_list')
    fields = ['position', 'organisation', 'description', 'location', 'phone_number', 'email']

    # def get(self, request, slug):
    #     object = self.model.objects.get(slug__iexact=slug)
    #     bound_form = self.form_model(instance=object)
    #     return render(request, self.template, context={
    #         'form': bound_form,
    #         self.model.__name__.lower(): object,
    #     })
    #     # form = self.form_model()
    #     # return render(request=request, template_name=self.template, context={'form': form})
    #
    # def post(self, request, slug):
    #     # prof_slug = request.build_absolute_uri().split('/')[-3]
    #     # bound_form = self.form_model(request.POST)
    #     # if bound_form.is_valid():
    #     #     profile = AgentProject.objects.get(url=slug)
    #     #     request.POST = request.POST.copy()
    #     #
    #     #     return redirect(self.success_url)
    #     # else:
    #     #     return render(request, self.template, context={'form': bound_form})
    #     object = self.model.objects.get(slug__iexact=slug)
    #     bound_form = self.form_model(request.POST, instance=object)
    #
    #     if bound_form.is_valid():
    #         new_object = bound_form.save()
    #         return redirect(new_object)
    #     return render(request, self.template, context={
    #         'form': bound_form,
    #         self.model.__name__.lower(): object,
    #     })


class UserEditView(LoginRequiredMixin, ObjectUpdateMixin, View):
    form_model = UserEditForm
    login_url = '/accounts/login'
    model = Profile
    template = 'user/user_edit.html'
    success_url = reverse_lazy('user')
    fields = ['tabel_num', 'position', 'phone_number']


class ProjectEditView(LoginRequiredMixin, ObjectUpdateMixin, View):
    form_model = ProjectEditForm
    login_url = '/accounts/login'
    model = Project
    template = 'project/project_edit.html'
    success_url = reverse_lazy('project')
    fields = ['status', 'description', 'tasks']


class HistoryAddView(LoginRequiredMixin, View):
    form_model = HistoryAddForm
    login_url = '/accounts/login'
    model = HistoryProject
    model_parent = Project
    template = 'project/project_add.html'
    success_url = reverse_lazy('project_list')
    fields = ['user_add', 'description', 'pub_date']

    def get(self, request, slug):
        profile = self.model_parent.objects.get(url=slug)
        form = self.form_model()
        return render(request=request, template_name=self.template, context={'form': form, 'project': profile})

    def right_date(self, date):
        date_formats_in = '%d.%m.%Y'
        date_formats_out = '%Y-%m-%d'
        result = datetime.strptime(date, date_formats_in).strftime(date_formats_out)
        return result

    def post(self, request, slug):
        # prof_slug = request.build_absolute_uri().split('/')[-3]
        bound_form = self.form_model(request.POST)
        if bound_form.is_valid():
            project = self.model_parent.objects.get(url=slug)
            request.POST = request.POST.copy()
            new_obj = self.model.objects.create(project=project,
                                                pub_date=self.right_date(request.POST['pub_date']),
                                                user_add=Profile.objects.get(pk=request.POST['user_add']),
                                                description=request.POST['description'],
                                                )
            new_obj.save()
            # profile.user_location = UserStatistic.objects.filter(user_name=profile).order_by('-pub_date')[:1][0]
            # profile.save()
            return redirect(self.success_url)
        else:
            return render(request, self.template, context={'form': bound_form})
