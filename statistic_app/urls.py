"""django_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from django.views.generic import RedirectView

from .views import UsersView, UserDetailView, UsersFilterView, UserStatistics, UserLocationAdd, ProjectsView, AgentView, \
    AgentDetailView, AgentEditView, ProjectDetailView

urlpatterns = [
    path('', RedirectView.as_view(url="/user/"), name='main_view'),
    path('statistics/', UserStatistics.as_view(), name='statistics'),
    path('filter/', UsersFilterView.as_view(), name='filter'),
    path('user/', UsersView.as_view(), name='user_list'),
    path('user/<str:slug>/', UserDetailView.as_view(), name='user_detail'),
    path('user/<str:slug>/update/', UserLocationAdd.as_view(), name='user_update'),
    path('project/', ProjectsView.as_view(), name='project_list'),
    path('project/<str:slug>/', ProjectDetailView.as_view(), name='project_detail'),
    path('agent/', AgentView.as_view(), name='agent_list'),
    path('agent/<str:slug>/', AgentDetailView.as_view(), name='agent_detail'),
    path('agent/<str:slug>/update/', AgentEditView.as_view(), name='agent_update'),
]
