from django.db import models

# Create your models here.
class Cliente(models.Model):
    ESTADOS = [
        ("Activo", "Activo"),
        ("Suspendido", "Suspendido"),
    ]
    GENEROS = [
        ("Masculino", "Masculino"),
        ("Femenino", "Femenino"),
        ("Otro", "Otro"),
    ]

    estado = models.CharField(max_length=15, choices=ESTADOS, default="Activo")
    nombre = models.CharField(max_length=100)
    genero = models.CharField(max_length=20, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    telefono = models.CharField(max_length=15, blank=True, null=True)
    celular = models.CharField(max_length=15, blank=True, null=True)
    correo = models.EmailField(blank=True, null=True)
    nit = models.CharField(max_length=20, unique=True)
    dui = models.CharField(max_length=10, unique=True)
    lugar_trabajo = models.CharField(max_length=100, blank=True, null=True)
    telefono_trabajo = models.CharField(max_length=15, blank=True, null=True)
    tipo_cliente = models.CharField(max_length=50, blank=True, null=True)
    estado_civil = models.CharField(max_length=50, blank=True, null=True)
    cargo_trabajo = models.CharField(max_length=50, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    colonia = models.CharField(max_length=100, blank=True, null=True)
    municipio = models.CharField(max_length=100, blank=True, null=True)
    ancho_bajada = models.CharField(max_length=20, blank=True, null=True)
    ancho_subida = models.CharField(max_length=20, blank=True, null=True)
    paquete = models.CharField(max_length=50, blank=True, null=True)
    olt = models.CharField(max_length=50, blank=True, null=True)
    referencia_nombre = models.CharField(max_length=100, blank=True, null=True)
    referencia_telefono = models.CharField(max_length=15, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.estado})"
