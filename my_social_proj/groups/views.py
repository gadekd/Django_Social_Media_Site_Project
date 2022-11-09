# GROUPS VIEWS

from django.shortcuts import render

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from django.urls import reverse
from django.views import generic
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.db import IntegityError

from gropus.models import Group, GroupMember

from . import models


class CreateGroup(LoginRequiredMixin, generic.CreateView):
    fields = ('name', 'description')
    model = Group
    

class SingleGroup(generic.DeleteView):
    model = Group
    

class ListGroups(generic.ListView):
    models = Group
    
    
class JoinGroup(LoginRequiredMixin, generic.RedirectView):
    
    def get_redirect_url(self, *args, **kwargs):
        """Get redirected to the page with detail view without particular group"""
        return reverse('groups:single', kwargs={'slug':self.kwargs.get('slug')})
    
    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))
        
        try:
            # Try to create a group member with the credentials the same as current user
            GroupMember.objects.create(user=self.request.user, group=group)
            
        except IntegityError:
            messages.warning(self.request, 'Warning! Already a member!')
        else:
            messages.success(self.request, 'You are now a member!')
            
            
class LeaveGroup(LoginRequiredMixin, generic.RedirectView):
    
    def get_redirect_url(self, *args, **kwargs):
        """Get redirected to the page with detail view without particular group"""
        return reverse('groups:single', kwargs={'slug':self.kwargs.get('slug')})
    
    def get(self, request, *args, **kwargs):
        
        try:
            membership = models.GroupMember.objects.filter(user=self.request.user, group__slug=self.kwargs.get('slug'))
        except models.GroupMember.DoesNotExist:
            messages.warning(self.request, 'Sorry, you are not a member of this group!')
        else:
            membership.delete()
            messages.success(self.request, 'You have successfully left the group!')
            
        return super().get(request, *args, **kwargs)     