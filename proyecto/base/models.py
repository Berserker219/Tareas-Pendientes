from django.db import models
from django.contrib.auth.models import User


# declaramos que esta clase es un modelo
class Tarea(models.Model):
    # ForeignKey se pone cuando tiene una cardinalidad de 
    # uno a muchos
    usuario = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                null =True,
                                blank=True) 
    titulo = models.CharField(max_length=200)
    description = models.TextField(null =True,
                                blank=True)
    completo =models.BooleanField(default=False)
    creado = models.DateTimeField(auto_now_add=True)

    # nos dice que si queremos que se imprima una tarea,
    # se va a imprimir el titulo creado
    def __str__(self):
        return self.titulo
   
    # ordering nos va indicar como se va ordenar las tareas 
    # dentro de nuestra tabla, el campo completo va a determinar
    # el orden
    class Meta:
        ordering = ['completo']