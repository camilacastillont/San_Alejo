from django.db import models

# Create your models here.
class Cliente(models.Model):
    ESTADOS = [
        ("Activo", "Activo"),
        ("Suspendido", "Suspendido"),
    ]

    estado = models.CharField(max_length=15, choices=ESTADOS, default="Activo")
    nombre = models.CharField(max_length=100)
    dui = models.CharField(max_length=10, unique=True)
    nit = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    celular = models.CharField(max_length=15, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.estado})"