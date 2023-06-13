from django.urls import path
from .views import ListarPostsView, DetallePostView, ListarCategoria, ListarSubBlogView,DetalleSubBlogView, CategoriaDetailView, FiltrarAgendaView

app_name = 'blog'

urlpatterns = [
    path('post', ListarPostsView.as_view(), name='listar_posts'),
    path('post/<int:pk>/', DetallePostView.as_view(), name='detalle_post'),
    path('categorias', ListarCategoria.as_view(),name='listar_categoria'),
    path('categoria/<slug:slug>/', CategoriaDetailView.as_view(), name='categoria'),
    path('subblog/<slug:slug>/', DetalleSubBlogView.as_view(), name='detalle_subblog'),
    path('api/filtrar-agenda/', FiltrarAgendaView.as_view(), name='filtrar_agenda_api'),
]