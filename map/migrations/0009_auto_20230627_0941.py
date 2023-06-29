from django.db import migrations, models


def set_default_post_ptr(apps, schema_editor):
    MapPoint = apps.get_model('map', 'MapPoint')
    Post = apps.get_model('blog', 'Post')

    for mappoint in MapPoint.objects.all():
        post = Post.objects.create()
        mappoint.post_ptr = post
        mappoint.save()


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0062_alter_post_titulo'),
        ('map', '0007_alter_mappoint_icono'),
    ]

    operations = [
        migrations.RunPython(set_default_post_ptr),
    ]
