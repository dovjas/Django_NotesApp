from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Note
# Create your views here.

class NotesList(LoginRequiredMixin,ListView):
    model = Note
    context_object_name = 'notes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes'] = context['notes'].filter(user=self.request.user)
        context['count'] = context['notes'].filter(note_complete=False).count()

        note_search_input = self.request.GET.get('note-search-input') or ''
        if note_search_input:
            context['notes'] = context['notes'].filter(note_title__startswith=note_search_input)

        return context

class NoteDetails(LoginRequiredMixin,DetailView):
    model = Note
    context_object_name = 'note'

class NoteCreate(LoginRequiredMixin, CreateView):
    model = Note
    fields = ['note_title','note_description','note_complete','note_image']
    success_url = reverse_lazy('notes')

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(NoteCreate,self).form_valid(form)

    def image_upload_view(request):
        """Process images uploaded by users"""
        if request.method == 'POST':
            form = Note(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                # Get the current instance object to display in the template
                img_obj = form.instance
                return render(request, 'note_detail.html', {'form': form, 'img_obj': img_obj})
        else:
            form = Note()
        return render(request, 'note_detail.html', {'form': form})


class NoteUpdate(LoginRequiredMixin,UpdateView):
    model = Note
    fields = ['note_title','note_description','note_complete','note_image']
    success_url = reverse_lazy('notes')

class NoteDelete(LoginRequiredMixin,DeleteView):
    model = Note
    context_object_name = 'note'
    success_url = reverse_lazy('notes')


#Login,Logout,Registration

class UserLogin(LoginView):
    template_name = 'notesApp/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('notes')

class UserRegistration(FormView):
    form_class = UserCreationForm
    template_name = 'notesApp/register.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('notes')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(UserRegistration, self).form_valid(form)