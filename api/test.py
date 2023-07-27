from django.test import TestCase, Client
from api.models import Teenvio, Subscriptor
from django.urls import reverse


class TeenvioModelTest(TestCase):
    def setUp(self):
        # Eliminar todas las instancias de Teenvio antes de ejecutar el test
        Teenvio.objects.all().delete()


    def test_get_singleton(self):
        teenvio = Teenvio.objects.create(gid="abc123", user="usuario1", password="secreto", plan="plan1", url="https://example.com/api", action="contact_save")
        teenvio2 = Teenvio.objects.get_singleton()
        self.assertEqual(teenvio, teenvio2)




    def test_post_request_invalid_email(self):
        # Crea una instancia de Client para simular una solicitud POST a la vista
        client = Client()
        response = client.post(reverse('api:newsletter'), data={'email': 'invalid_email'})

        # Verifica que la respuesta sea un JSON con un mensaje de error
        self.assertJSONEqual(response.content, {'error': 'Dirección de correo electrónico inválida'})


class SubscriptorModelTest(TestCase):
    def test_subscriptor_str(self):
        # Crea un objeto Subscriptor
        subscriptor = Subscriptor.objects.create(name='John Doe', email='john@example.com')

        # Asegúrate de que el método __str__ funcione correctamente
        self.assertEqual(str(subscriptor), 'John Doe')
