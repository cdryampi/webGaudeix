from django.test import TestCase
from blog.models import Tag
from django.core.exceptions import ValidationError
from blog.models import SubBlog, SubBlogImagen
from django.contrib.auth import get_user_model
from django.urls import reverse
from multimedia_manager.models import Imagen
from django.core.files.uploadedfile import SimpleUploadedFile


class TagModelTest(TestCase):

    def test_crear_tag(self):
        # Crea un nuevo objeto Tag y guárdalo en la base de datos
        tag = Tag.objects.create(nombre="Python")

        # Verifica que el objeto se haya guardado correctamente
        self.assertEqual(tag.nombre, "Python")

    def test_longitud_maxima_nombre(self):
        # Creamos un objeto Tag con un nombre que tenga la longitud máxima permitida (255 caracteres)
        nombre_maximo = 'a' * 255
        tag = Tag(nombre=nombre_maximo)

        # Verificamos que el guardado del objeto no lance la excepción ValidationError
        try:
            tag.save()
        except ValidationError:
            self.fail("El guardado con nombre de longitud 255 falló.")


class SubBlogModelTest(TestCase):

    def setUp(self):
        # Configuración inicial para las pruebas
        User = get_user_model()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.subblog = SubBlog.objects.create(
            titulo='SubBlog de Prueba',
            contenido='Contenido del SubBlog de Prueba',
            publicado=True,
            creado_por=self.user
        )

    def test_actualizar_subblog_existente(self):
        # Prueba de actualización de un SubBlog existente
        self.subblog.titulo = 'SubBlog Actualizado'
        self.subblog.contenido = 'Contenido Actualizado'
        self.subblog.save()

        subblog_actualizado = SubBlog.objects.get(id=self.subblog.id)
        self.assertEqual(subblog_actualizado.titulo, 'SubBlog Actualizado')
        self.assertEqual(subblog_actualizado.contenido, 'Contenido Actualizado')

    def test_eliminar_subblog(self):
        # Prueba de eliminación de un SubBlog
        self.subblog.delete()

        with self.assertRaises(SubBlog.DoesNotExist):
            SubBlog.objects.get(id=self.subblog.id)

    def test_view_on_site(self):
        subblog = SubBlog.objects.create(titulo="Mi Subblog")
        response = self.client.get(subblog.get_absolute_url())

        # Verificar que la respuesta tenga un código de estado 200
        self.assertEqual(response.status_code, 200)

    def test_guardar_sin_titulo(self):
        # Prueba de guardado sin título
        with self.assertRaises(ValueError):
            subblog = SubBlog.objects.create(
                contenido='Contenido sin título',
                publicado=True,
                creado_por=self.user
            )
    def test_guardar_sin_contenido(self):
        # Prueba de guardado sin contenido
        subblog = SubBlog.objects.create(
            titulo='SubBlog Sin Contenido',
            publicado=True,
            creado_por=self.user
        )
        self.assertIsNotNone(subblog)
    @classmethod
    def setUpTestData(cls):
        # Creamos un usuario para usarlo en las pruebas
        User = get_user_model()

    def test_create_subblog(self):
        # Creamos un nuevo subblog
        subblog = SubBlog.objects.create(
            titulo='Nuevo SubBlog',
            contenido='Contenido del SubBlog',
            publicado=True,
        )

        # Verificamos que el objeto se haya creado correctamente
        self.assertTrue(isinstance(subblog, SubBlog))
        self.assertEqual(subblog.titulo, 'Nuevo SubBlog')
        self.assertEqual(subblog.contenido, 'Contenido del SubBlog')
        self.assertTrue(subblog.publicado)
        self.assertEqual(subblog.creado_por, self.user)
        self.assertEqual(subblog.modificado_por, self.user)

    def test_slug_creation(self):
        # Creamos un subblog con un título
        subblog = SubBlog.objects.create(titulo="Mi Subblog")
        
        # Verificamos que el slug no está vacío
        self.assertIsNotNone(subblog.slug)

        # Verificamos que el slug es único en la base de datos
        self.assertTrue(SubBlog.objects.filter(slug=subblog.slug).exists())

    def test_get_absolute_url(self):
        # Creamos un subblog
        subblog = SubBlog.objects.create(
            titulo='Nuevo SubBlog',
            contenido='Contenido del SubBlog',
            publicado=True,
        )

        # Verificamos que el método get_absolute_url devuelva la URL correcta
        expected_url = f'/subblog/{subblog.slug}/'
        self.assertEqual(subblog.get_absolute_url(), expected_url)



class SubBlogImagenModelTest(TestCase):
    def setUp(self):
        # Creamos una instancia de SubBlog y la guardamos en la base de datos
        self.subblog = SubBlog.objects.create(titulo="Mi Subblog")
        
        # Creamos un archivo temporal en memoria para asignarlo al campo archivo de la instancia de Imagen
        archivo_temporal = SimpleUploadedFile(
            "imagen_prueba.jpg",
            b"contenido_de_prueba",
            content_type="image/jpeg"
        )
        
        # Creamos una instancia de Imagen y la guardamos en la base de datos
        self.imagen = Imagen.objects.create(titulo="Imagen de prueba", archivo=archivo_temporal)
        
    def test_creacion_subblog_imagen(self):
        # Creamos una instancia de SubBlogImagen relacionando el SubBlog y la Imagen creados anteriormente
        subblog_imagen = SubBlogImagen.objects.create(subblog=self.subblog, imagen=self.imagen)
        
        # Verificamos que la creación fue exitosa
        self.assertEqual(subblog_imagen.subblog, self.subblog)
        self.assertEqual(subblog_imagen.imagen, self.imagen)
        
    def test_eliminar_subblog_imagen(self):
        # Creamos una instancia de SubBlogImagen relacionando el SubBlog y la Imagen creados anteriormente
        subblog_imagen = SubBlogImagen.objects.create(subblog=self.subblog, imagen=self.imagen)
        
        # Verificamos que la relación se creó correctamente
        self.assertEqual(subblog_imagen.subblog, self.subblog)
        self.assertEqual(subblog_imagen.imagen, self.imagen)
        
        # Eliminamos la instancia de SubBlogImagen
        subblog_imagen.delete()
        
        # Verificamos que la instancia de SubBlogImagen se eliminó correctamente
        with self.assertRaises(SubBlogImagen.DoesNotExist):
            SubBlogImagen.objects.get(subblog=self.subblog, imagen=self.imagen)
