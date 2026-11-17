from django.contrib import admin
from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Encargos, Linea, Producto


class AdministracionTests(TestCase):
    def setUp(self):
        self.client.force_login(get_user_model().objects.create_superuser(
            username='admin', email='admin@example.com', password='test-admin',
        ))
        self.linea = Linea.objects.create(nombre='Postres')

    def test_admin_rechaza_lineas_repetidas(self):
        for nombre in ['Postres', 'postres', 'POSTRES', ' Postres ']:
            with self.subTest(nombre=nombre):
                response = self.client.post(reverse('admin:pasteleria_linea_add'), {'nombre': nombre})
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'Ya existe una línea con este nombre.')
                self.assertEqual(Linea.objects.count(), 1)

    def test_base_de_datos_rechaza_duplicados(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Linea.objects.create(nombre='postres')

    def test_editar_linea_conservando_nombre(self):
        self.linea.full_clean()
        response = self.client.post(
            reverse('admin:pasteleria_linea_change', args=[self.linea.pk]),
            {'nombre': 'Postres'},
        )
        self.assertEqual(response.status_code, 302)

    def test_listado_encargos_muestra_datos_solicitados(self):
        producto = Producto.objects.create(
            id=123, Linea=self.linea, nombre='Flan', descripcion='Vainilla',
            porciones=4, stock=10, precio=5000, disponibleparaventa=True,
        )
        encargo = Encargos.objects.create(
            producto=producto, nombre='Ana Pérez', correo='ana@example.com',
            fechapedido=timezone.localdate(), fecharetiro=timezone.localdate(),
            unidadesApedir=2,
        )
        response = self.client.get(reverse('admin:pasteleria_encargos_changelist'))
        self.assertEqual(response.status_code, 200)
        for texto in ['Código de producto', 'Producto', 'Nombre', 'Flan', 'Ana Pérez', '123']:
            self.assertContains(response, texto)
        model_admin = admin.site._registry[Encargos]
        self.assertEqual(model_admin.codigo(encargo), producto.pk)
        self.assertContains(response, 'field-unidadesApedir">2</td>')
        self.assertContains(response, 'field-fecharetiro')
