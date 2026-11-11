from django.db import models

class Linea(models.Model):
    nombre = models.CharField(max_length=30)

class Producto(models.Model):
    Linea = models.ForeignKey(
        Linea,
        on_delete=models.CASCADE
    )
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField()
    imagen = models.ImageField(null=True)
    porciones = models.SmallIntegerField()
    aptocelíacos = models.BooleanField(default=False)
    stock = models.SmallIntegerField()
    precio = models.IntegerField()
    disponibleparaventa = models.BooleanField()
