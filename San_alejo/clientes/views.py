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
