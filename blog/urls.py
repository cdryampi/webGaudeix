from django.urls import path
from .views import ListarPostsView, DetallePostView, ListarCategoria, ListarSubBlogView,DetalleSubBlogView, CategoriaDetailView, FiltrarAgendaView, DetalleNoticiaView, ListarNoticiaView, SubCategoriaDetailView, RestaurantAPI


app_name = 'blog'

urlpatterns = [
    path('posts/', ListarPostsView.as_view(), name='listar_posts'),
    path('post/<slug:slug>/', DetallePostView.as_view(), name='detalle_post'),
    path('categorias/', ListarCategoria.as_view(),name='listar_categoria'),
    path('c/<slug:slug>/', CategoriaDetailView.as_view(), name='categoria'),
    path('subblog/<slug:slug>/', DetalleSubBlogView.as_view(), name='detalle-subblog'),
    # API endpoints
    path('api/filtrar-agenda/', FiltrarAgendaView.as_view(), name='filtrar_agenda_api'),
    path('api/filtrar-restaurante/', RestaurantAPI.as_view(), name='filtrar_restaurante'),
    path('noticies/', ListarNoticiaView.as_view(), name="noticies"),
    path('n/<slug:slug>/', DetalleNoticiaView.as_view(), name='noticia'),
    path('subcategoria/<slug:slug>/', SubCategoriaDetailView.as_view(), name='subcategoria')
]