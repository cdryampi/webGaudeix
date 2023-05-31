from django.urls import path
from .views import ListarPostsView, DetallePostView, ListarCategoria, ListarSubBlogView,DetalleSubBlogView, CategoriaDetailView

app_name = 'blog'

urlpatterns = [
    path('post', ListarPostsView.as_view(), name='listar_posts'),
    path('post/<int:pk>/', DetallePostView.as_view(), name='detalle_post'),
    path('categorias', ListarCategoria.as_view(),name='listar_categoria'),
    path('categoria/<int:categoria_id>/', CategoriaDetailView.as_view(), name='categoria'),
    path('subblog/<int:subblog_id>/', DetalleSubBlogView.as_view(), name='detalle_subblog'),
]