from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.index, name='clientes'),
    path("listado/", views.listado_clientes, name="listado_clientes"),
    path('agregar/', views.agregar_cliente, name='agregar_cliente')


]