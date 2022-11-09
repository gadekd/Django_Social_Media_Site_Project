from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.urls import reverse
from django.views import generic

from gropus.models import Group, GroupMember


class CreateGroup(LoginRequiredMixin, generic.CreateView):
    fields = ('name', 'description')
    model = Group
    

class SingleGroup(generic.DeleteView):
    model = Group
    

class ListGroups(generic.ListView):
    models = Group