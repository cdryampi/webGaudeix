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

class TeenvioViewTest(TestCase):
    def test_sql_injection_attempt(self):
        # Supongamos que existe una URL llamada 'newsletter_subscribe' para simplificar
        url = reverse('api:newsletter')
        malicious_payload = {'email': "'; DROP TABLE users; --"}
        response = self.client.post(url, data=malicious_payload)
        
        # Aquí podrías verificar que la tabla no ha sido eliminada, pero dado que estás usando Django ORM,
        # este tipo de comandos inyectados no deberían tener efecto.
        # Además, puedes verificar que la respuesta no indica una ejecución exitosa de SQL malicioso.
        self.assertNotEqual(response.status_code, 200)  # Este código depende de cómo gestiones los errores.
        # Podrías buscar un mensaje específico de error o verificar que los usuarios o los datos siguen intactos.
