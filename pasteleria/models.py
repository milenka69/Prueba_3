from django.db import models

class Linea(models.Model):
    nombre = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    Linea = models.ForeignKey(
        Linea,
        on_delete=models.CASCADE
    )
    nombre = models.CharField(max_length=30)
    descripcion = models.TextField()
    imagen = models.ImageField(null=True)
    porciones = models.SmallIntegerField()
    aptoceliacos = models.BooleanField(default=False)
    stock = models.SmallIntegerField()
    precio = models.IntegerField()
    disponibleparaventa = models.BooleanField()

    def __str__(self):
        return self.nombre

class Encargos(models.Model):
    nombre = models.CharField(max_length=50)
    telefono = models.CharField(max_length=15)
    correo = models.EmailField()
    fechapedido = models.DateField()
    fecharetiro = models.TimeField()
    unidadesApedir = models.SmallIntegerField()
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE
    )
    def __str__(self):
        return self.nombre