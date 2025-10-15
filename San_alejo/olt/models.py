from django.db import models
from django.db.models import Max

# Create your models here.
class Tarjeta(models.Model):
    slot = models.CharField(max_length=10)
    nombre = models.CharField(max_length=50)
    
    ESTADOS = [
        ("Normal", "Normal"),
        ("Falla", "Falla"),
    ]
    estado = models.CharField(max_length=10, choices=ESTADOS, default="Normal")

    POWER_ESTADOS = [
        ("POWER-ON", "POWER-ON"),
        ("POWER-OFF", "POWER-OFF"),
    ]
    power = models.CharField(max_length=10, choices=POWER_ESTADOS, default="POWER-ON")

    def __str__(self):
        return f"{self.slot} - {self.nombre}"
    
class Puerto(models.Model):
    tarjeta = models.ForeignKey(Tarjeta, on_delete=models.CASCADE, related_name="puertos")
    numero = models.IntegerField(default=0) 
    port = models.CharField(max_length=10)
    tipo = models.CharField(max_length=20)
    min_distance = models.DecimalField(max_digits=5, decimal_places=2)
    max_distance = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=20, default="Offline")

    def __str__(self):
        return f"Puerto {self.port} - {self.tarjeta.nombre}"
    
class ONT(models.Model):
    puerto = models.ForeignKey("Puerto", on_delete=models.CASCADE, related_name="onts")
    ont_id = models.PositiveIntegerField()
    service_port = models.PositiveIntegerField(unique=True)
    nombre = models.CharField(max_length=100)
    sn = models.CharField(max_length=100)

    control_flag = models.CharField(max_length=50, default="active")

    run_state = models.CharField(
        max_length=50,
        choices=[("Online", "Online"), ("Offline", "Offline")],
        default="Offline",
    )

    config_state = models.CharField(
        max_length=50,
        default="Initial",
        blank=True,
        null=True
    )

    match_state = models.CharField(
        max_length=50,
        choices=[("Match", "Match"), ("Mismatch", "Mismatch"), ("Initial", "Initial")],
        default="Initial",
    )

    protect_side = models.CharField(max_length=50, blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Reglas automáticas:
        - service_port se autoincrementa globalmente.
        - ont_id se autoincrementa por puerto (reinicia en cada puerto).
        - evita agregar ONTs si el puerto está lleno (64 como máximo).
        """

        # Autoincrementar service_port global
        if not self.service_port:
            max_sp = ONT.objects.aggregate(max_sp=Max("service_port"))["max_sp"]
            self.service_port = (max_sp or 0) + 1

        # Autoincrementar ont_id por puerto
        if not self.ont_id:
            max_ont = ONT.objects.filter(puerto=self.puerto).aggregate(max_ont=Max("ont_id"))["max_ont"]
            self.ont_id = (max_ont or 0) + 1

        # Limitar capacidad del puerto
        if ONT.objects.filter(puerto=self.puerto).count() >= 64:
            raise ValueError(f"El puerto {self.puerto.port} ya alcanzó el límite de 64 ONTs.")

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} (ONT {self.ont_id} - Puerto {self.puerto.port})"