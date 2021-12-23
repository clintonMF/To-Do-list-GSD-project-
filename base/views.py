from django.shortcuts import render,redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from .models import task
from django.urls import reverse_lazy


from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from datetime import date

# Create your views here.



class customloginview( LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks')
    
class registerpage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(registerpage, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(registerpage, self).get(*args, **kwargs)
    
class tasklist(LoginRequiredMixin, ListView):
    model = task
    context_object_name = 'tasks'
    
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        
        search_input = self.request.GET.get('search-area') or ""
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)
            
            
        context['search_input']= search_input
        
        return context
    
    
class taskdetail(LoginRequiredMixin, DetailView):
    model = task
    context_object_name = 'customtask'
    template_name = 'base/task.html'
    
class taskcreate(LoginRequiredMixin, CreateView):
    model = task
    fields = ['title','description','complete',]
    success_url = reverse_lazy('tasks')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(taskcreate, self).form_valid(form)
    
class taskupdate(LoginRequiredMixin, UpdateView):
    model = task
    fields = ['title','description','complete']
    success_url = reverse_lazy('tasks')
    
class taskdelete(LoginRequiredMixin, DeleteView):
    model = task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks') 
    
    
       
def home(request):
    return render(request,'task_list.html',{'clinton': date.today()})