from django.core.management.base import BaseCommand
from django.utils.text import slugify
from blog.models import Post

class Command(BaseCommand):
    help = 'Assign slugs to existing Post objects'

    def handle(self, *args, **options):
        posts = Post.objects.all()
        for post in posts:
            # Generar el slug basado en el título
            slug = slugify(post.titulo)
            post.slug = slug
            post.save()
