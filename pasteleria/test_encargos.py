from datetime import timedelta

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Encargos, Linea, Producto


class EncargoTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        linea = Linea.objects.create(nombre='Tortas')
        cls.producto = Producto.objects.create(
            Linea=linea, nombre='Torta', descripcion='Chocolate',
            porciones=8, stock=10, precio=15000, disponibleparaventa=True,
        )

    def setUp(self):
        self.detalle_url = reverse('detalle', args=[self.producto.pk])
        self.url = reverse('encargar', args=[self.producto.pk])
        self.datos = {
            'nombre': 'Ana Pérez', 'correo': 'ana@example.com',
            'fecharetiro': timezone.localdate().strftime('%d/%m/%Y'), 'unidadesApedir': 1,
        }

    def test_formulario_publico(self):
        detalle = self.client.get(self.detalle_url)
        self.assertContains(detalle, f'href="{self.url}"')
        self.assertContains(detalle, '>Encargar</a>')
        self.assertNotContains(detalle, 'name="fecharetiro"')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="fecharetiro"')
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        self.assertContains(response, 'Dia/Mes/Año')
        self.assertEqual(Encargos.objects.count(), 0)

    def test_encargos_validos_sin_sesion(self):
        for unidades, dias in [(1, 0), (3, 1)]:
            with self.subTest(unidades=unidades, dias=dias):
                datos = dict(self.datos, unidadesApedir=unidades,
                             fecharetiro=(timezone.localdate() + timedelta(days=dias)).strftime('%d/%m/%Y'))
                response = self.client.post(self.url, datos, follow=True)
                self.assertRedirects(response, self.detalle_url)
                self.assertContains(response, 'Tu encargo fue registrado correctamente.')
                encargo = Encargos.objects.latest('pk')
                self.assertEqual(encargo.producto, self.producto)
                self.assertEqual(encargo.fechapedido, timezone.localdate())
                self.assertEqual(encargo.fecharetiro.strftime('%d/%m/%Y'), datos['fecharetiro'])
                self.assertEqual(encargo.unidadesApedir, unidades)
                self.assertEqual(encargo.nombre, datos['nombre'])
                self.assertEqual(encargo.correo, datos['correo'])
        self.assertEqual(Encargos.objects.count(), 2)
        self.client.get(self.url)
        self.assertEqual(Encargos.objects.count(), 2)

    def test_datos_invalidos_muestran_error_y_no_guardan(self):
        casos = [
            ('unidadesApedir', '0'), ('unidadesApedir', '4'),
            ('unidadesApedir', '1.5'), ('unidadesApedir', 'abc'),
            ('correo', 'correo-invalido'), ('correo', ''), ('nombre', ''),
            ('fecharetiro', (timezone.localdate() - timedelta(days=1)).strftime('%d/%m/%Y')),
            ('fecharetiro', '31/02/2027'),
            ('fecharetiro', timezone.localdate().isoformat()),
            ('fecharetiro', 'fecha-invalida'), ('fecharetiro', ''),
        ]
        for campo, valor in casos:
            with self.subTest(campo=campo, valor=valor):
                response = self.client.post(self.url, dict(self.datos, **{campo: valor}))
                self.assertEqual(response.status_code, 200)
                self.assertIn(campo, response.context['form'].errors)
                self.assertContains(response, 'errorlist')
                contenido = response.content.decode()
                self.assertLess(
                    contenido.index(f'id="id_{campo}"'),
                    contenido.index(f'id="id_{campo}_error"'),
                )
                if campo == 'correo' and valor:
                    self.assertContains(response, 'Ingresa un correo electrónico válido.')
                self.assertEqual(Encargos.objects.count(), 0)

    def test_fecha_conserva_dia_y_mes_al_mostrar_error(self):
        datos = dict(self.datos, fecharetiro='05/06/2030', correo='invalido')
        response = self.client.post(self.url, datos)
        self.assertContains(response, 'value="05/06/2030"')
        self.assertEqual(response.context['form'].cleaned_data['fecharetiro'].day, 5)
        self.assertEqual(response.context['form'].cleaned_data['fecharetiro'].month, 6)
        self.assertEqual(Encargos.objects.count(), 0)

    def test_producto_no_disponible_no_admite_encargos(self):
        self.producto.disponibleparaventa = False
        self.producto.save()
        response = self.client.post(self.url, self.datos)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Encargos.objects.count(), 0)
