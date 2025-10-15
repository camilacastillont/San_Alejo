from django.urls import path
from . import views

app_name = 'olt'

urlpatterns = [
   # path('', views.index, name='olt'),
    path('', views.index, name='san_alejo'),
    path('agregar/', views.agregar_tarjeta, name='agregar_tarjeta'),
    path("tarjeta/<int:pk>/", views.detalle_tarjeta, name="detalle_tarjeta"),
    path('eliminar_tarjeta/<int:pk>/', views.eliminar_tarjeta, name='eliminar_tarjeta'),
]