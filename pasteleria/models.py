from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.functions import Lower, Trim
from django.utils import timezone

class Linea(models.Model):
    nombre = models.CharField(max_length=30)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                Lower(Trim('nombre')), name='linea_nombre_unico',
                violation_error_message='Ya existe una línea con este nombre.',
            ),
        ]

    def clean(self):
        super().clean()
        self.nombre = self.nombre.strip()
        if Linea.objects.filter(nombre__iexact=self.nombre).exclude(pk=self.pk).exists():
            raise ValidationError({'nombre': 'Ya existe una línea con este nombre.'})

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    Linea = models.ForeignKey(
        Linea,
        on_delete=models.CASCADE
    )
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)
    porciones = models.SmallIntegerField()
    aptoceliacos = models.BooleanField(default=False)
    stock = models.SmallIntegerField()
    precio = models.IntegerField()
    disponibleparaventa = models.BooleanField()

    def __str__(self):
        return self.nombre

class Encargos(models.Model):
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15, blank=True)
    correo = models.EmailField()
    fechapedido = models.DateField()
    fecha_hora = models.DateTimeField(default=timezone.now, null=True, editable=False)
    total = models.IntegerField(null=True, editable=False)
    fecharetiro = models.DateField()
    unidadesApedir = models.SmallIntegerField()
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE
    )
    def __str__(self):
        return self.nombre
