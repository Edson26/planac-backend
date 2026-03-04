from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    ROL_CHOICES = [("coordinador", "Coordinador"), ("docente", "Docente")]
    rol = models.CharField(max_length=20, choices=ROL_CHOICES, default="docente")
    horas_contrato = models.FloatField(default=0)

    def __str__(self):
        return f"{self.get_full_name()} ({self.rol})"


class Planificacion(models.Model):
    anio = models.IntegerField()
    semestre = models.IntegerField(choices=[(1, "Primer Semestre"), (2, "Segundo Semestre")])
    activo = models.BooleanField(default=True)
    fecha_cierre = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ("anio", "semestre")

    def __str__(self):
        return f"PLANAC {self.anio} - {self.get_semestre_display()}"


class Asignatura(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=200)
    num_estudiantes = models.IntegerField(default=0)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"


class ModuloAsignatura(models.Model):
    TIPO_CHOICES = [
        ("tutoria", "Tutoría"),
        ("clase", "Clase"),
        ("grupo_practica", "Grupo Práctica"),
        ("encargatura", "Encargatura"),
    ]
    UNIDAD_CHOICES = [("periodos", "Períodos"), ("grupos", "Grupos")]

    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE, related_name="modulos")
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    unidad = models.CharField(max_length=20, choices=UNIDAD_CHOICES, default="grupos")
    factor_d = models.FloatField(help_text="Horas directas por unidad")
    factor_i = models.FloatField(default=0, help_text="Horas indirectas por unidad")
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.asignatura.codigo} - {self.nombre}"


class CargaDocente(models.Model):
    planificacion = models.ForeignKey(Planificacion, on_delete=models.CASCADE, related_name="cargas")
    docente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="cargas")
    modulo = models.ForeignKey(ModuloAsignatura, on_delete=models.CASCADE)
    cantidad = models.FloatField(default=0, help_text="Número de períodos o grupos")
    observaciones = models.TextField(blank=True)

    class Meta:
        unique_together = ("planificacion", "docente", "modulo")

    @property
    def horas_directas(self):
        return self.cantidad * self.modulo.factor_d

    @property
    def horas_indirectas(self):
        return self.cantidad * self.modulo.factor_i

    @property
    def horas_total(self):
        return self.horas_directas + self.horas_indirectas

    def __str__(self):
        return f"{self.docente} - {self.modulo} ({self.cantidad})"


class OtraActividad(models.Model):
    planificacion = models.ForeignKey(Planificacion, on_delete=models.CASCADE, related_name="otras_actividades")
    docente = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="otras_actividades")
    descripcion = models.TextField()
    horas = models.FloatField()
    tiene_resolucion = models.BooleanField(default=False)
    tiene_respaldo = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.docente} - {self.descripcion[:40]}"
