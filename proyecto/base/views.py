from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login 
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Tarea

# Vista de logueo
class Logueo(LoginView):
    template_name = 'base/login.html'
    field = '__all__'
    # reedireccionar al usario autenticado
    redirect_authenticated_user = True
    # cuando el usuario sea logueeado ira directamente a la pagina de tareas
    def get_success_url(self):
        return reverse_lazy('tareas')

# Vista de registro
class PaginaRegistro(FormView):
    template_name = 'base/registro.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True   
    success_url = reverse_lazy('tareas')
    
    def form_valid(self, form):
        usuario = form.save()
        if usuario is not None:
            login(self.request,usuario)
        return super(PaginaRegistro,self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tareas')
        return super(PaginaRegistro, self).get(*args,**kwargs)
    

# LoginRequiredMixin va a hacer es restringir si no tienes permiso para verlo
# ListView es una vista que nos permite ver una lista de objetos
class ListaPendientes(LoginRequiredMixin, ListView):
    model = Tarea    
    context_object_name = 'tareas'
        # **kwargs son elementos que tengan palabras claves
    def get_context_data(self, **kwargs):
        # super es estancia superior
        context = super().get_context_data(**kwargs)
        context['tareas'] = context['tareas'].filter(usuario=self.request.user)
        context['count'] = context['tareas'].filter(completo=False).count()
        # solo mostrar tareas que el usuario busco
        valor_buscado = self.request.GET.get('area-buscar') or ''
        if valor_buscado:
            # vamos a buscar que en titulo contengan a valor buscado
           
            context['tareas'] = context['tareas'].filter(titulo__icontains=valor_buscado)
        context['valor_buscado'] = valor_buscado
        return context

# DetalleTarea es una vista que nos permite ver los detalles de la tarea
class DetalleTarea(LoginRequiredMixin, DetailView):
    model = Tarea
    context_object_name = 'tarea'

# CrearTarea es una vista que nos permite crear una tarea
class CrearTarea(LoginRequiredMixin, CreateView):
    model = Tarea
    fields = ['titulo', 'description', 'completo']
    # reverse_lazy hace es redirigirte a un enlace que tu decidas
    # mediante un evento
    success_url = reverse_lazy('tareas')  

    def form_valid(self, form):
        # se le asignara la tarea creada al usuario quien la creo
        form.instance.usuario = self.request.user
        return super(CrearTarea, self).form_valid(form)

# EditarTarea es una vista que nos permite editar una tarea
class EditarTarea(LoginRequiredMixin, UpdateView):
    model = Tarea
    fields = ['titulo', 'description', 'completo']
    # reverse_lazy hace es redirigirte a un enlace que tu decidas
    # mediante un evento
    success_url = reverse_lazy('tareas') 

# EliminarTarea es una vista que nos permite eliminar una tarea
class EliminarTarea(LoginRequiredMixin, DeleteView):
    model = Tarea
    context_object_name = 'tarea'
    success_url = reverse_lazy('tareas')

