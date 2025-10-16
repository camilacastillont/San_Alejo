from django.shortcuts import render
from django.http import JsonResponse
from .models import Cliente
from django.views.decorators.csrf import csrf_exempt

def index(request):
    # Puedes redirigir directamente al listado de clientes o mostrar algo básico
    return render(request, "clientes/index.html")

def listado_clientes(request):
    query = request.GET.get("q", "")
    clientes = Cliente.objects.all()

    if query:
        clientes = clientes.filter(nombre__icontains=query)

    context = {
        "clientes": clientes,
        "query": query,
    }
    return render(request, "clientes/listado_clientes.html", context)

@csrf_exempt
def agregar_cliente(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        dui = request.POST.get("dui")
        nit = request.POST.get("nit")
        telefono = request.POST.get("telefono")
        celular = request.POST.get("celular")
        estado = request.POST.get("estado")

        cliente = Cliente.objects.create(
            nombre=nombre,
            dui=dui,
            nit=nit,
            telefono=telefono,
            celular=celular,
            estado=estado
        )

        data = {
            "id": cliente.id,
            "nombre": cliente.nombre,
            "dui": cliente.dui,
            "nit": cliente.nit,
            "telefono": cliente.telefono,
            "celular": cliente.celular,
            "estado": cliente.estado
        }
        return JsonResponse(data)
    return JsonResponse({"error": "Método no permitido"}, status=400)

def detalle_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    return render(request, 'clientes/detalle_clientes.html', {'cliente': cliente})

def actualizar_cliente(request, cliente_id):
    if request.method == 'POST':
        cliente = get_object_or_404(Cliente, id=cliente_id)
        data = request.POST

        # Actualizar campos
        cliente.nombre = data.get('nombre')
        cliente.genero = data.get('genero')
        cliente.fecha_nacimiento = data.get('fecha_nacimiento')
        cliente.telefono = data.get('telefono')
        cliente.celular = data.get('celular')
        cliente.correo = data.get('correo')
        cliente.lugar_trabajo = data.get('lugar_trabajo')
        cliente.telefono_trabajo = data.get('telefono_trabajo')
        cliente.tipo_cliente = data.get('tipo_cliente')
        cliente.estado_civil = data.get('estado_civil')
        cliente.cargo_trabajo = data.get('cargo_trabajo')
        cliente.direccion = data.get('direccion')
        cliente.colonia = data.get('colonia')
        cliente.municipio = data.get('municipio')
        cliente.ancho_bajada = data.get('ancho_bajada')
        cliente.ancho_subida = data.get('ancho_subida')
        cliente.paquete = data.get('paquete')
        cliente.olt = data.get('olt')
        cliente.referencia_nombre = data.get('referencia_nombre')
        cliente.referencia_telefono = data.get('referencia_telefono')
        cliente.save()

        return JsonResponse({'success': True, 'message': 'Cliente actualizado correctamente'})
    return JsonResponse({'success': False, 'message': 'Método no permitido'})
