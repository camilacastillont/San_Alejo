from django.urls import path
from . import views

app_name = 'olt'

urlpatterns = [
   
    path('', views.index, name='san_alejo'),
    path('onts/', views.detalle_tarjeta, name='onts'),
    path('agregar/', views.agregar_tarjeta, name='agregar_tarjeta'),
    path('tarjeta/<int:tarjeta_id>/', views.detalle_tarjeta, name='detalle_tarjeta'),
    path('eliminar_tarjeta/<int:pk>/', views.eliminar_tarjeta, name='eliminar_tarjeta'),
    path('tarjeta/<int:tarjeta_id>/puerto/agregar/', views.agregar_puerto, name='agregar_puerto'),
    path('tarjetas/puerto/<int:puerto_id>/ont/agregar/', views.agregar_ont, name='agregar_ont'),
]
