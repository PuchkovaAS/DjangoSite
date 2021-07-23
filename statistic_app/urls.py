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

from .views import index, UsersView, UserDetailView, UserLocationAdd, UsersFilterView

urlpatterns = [
    path('', RedirectView.as_view(url="/user/"), name='main_view'),
    path('filter/', UsersFilterView.as_view(), name='filter'),
    path('user/', UsersView.as_view(), name='user_list'),
    path('user/<str:slug>/', UserDetailView.as_view(), name='user_detail'),
    path('user/<str:slug>/update/', UserLocationAdd.as_view(), name='user_update'),

]
