from .models import Tarjeta, Puerto, ONT
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse, request, response
from django.views.decorators.http import require_POST

def index(request):
    return san_alejo(request) 

def san_alejo(request):
    tarjetas = Tarjeta.objects.all().order_by("slot")
    query = request.GET.get("q", "").strip()

    if query:
        # Buscar por slot (exacto)
        tarjetas = Tarjeta.objects.filter(slot__iexact=query).order_by("slot")
        print(f" Buscando '{query}' → {tarjetas.count()} resultados")
    else:
        # Mostrar todas las tarjetas
        tarjetas = Tarjeta.objects.all().order_by("slot")

    context = {
        "tarjetas": tarjetas,
        "query": query,
    }

    return render(request, "san_alejo.html", context)
def detalle_tarjeta(request, pk):
    tarjeta = get_object_or_404(Tarjeta, pk=pk)
    ports = tarjeta.puertos.all().order_by("numero")
    onts = ONT.objects.filter(puerto__tarjeta=tarjeta)

    # --- Si el formulario se envía vía AJAX (fetch) ---
    if request.method == "POST" and request.headers.get("x-requested-with") == "XMLHttpRequest":
        port = request.POST.get("port")
        tipo = request.POST.get("tipo")
        min_distance = request.POST.get("min_distance")
        max_distance = request.POST.get("max_distance")
        status = request.POST.get("status")

        nuevo_puerto = Puerto.objects.create(
            tarjeta=tarjeta,
            numero=port,
            tipo=tipo,
            min_distance=min_distance,
            max_distance=max_distance,
            status=status,
        )

        # --- Devolver los datos del nuevo puerto en JSON ---
        return JsonResponse({
            "id": nuevo_puerto.id,
            "numero": nuevo_puerto.numero,
            "tipo": nuevo_puerto.tipo,
            "min_distance": nuevo_puerto.min_distance,
            "max_distance": nuevo_puerto.max_distance,
            "status": nuevo_puerto.status,
        })

    # --- Si es GET, simplemente mostrar la plantilla ---
    return render(request, "detalle_tarjeta.html", {
        "tarjeta": tarjeta,
        "ports": ports,
        "onts": onts,
    })

@csrf_protect
def agregar_tarjeta(request):
    if request.method == "POST":
        slot = request.POST.get("slot")
        nombre = request.POST.get("nombre")
        estado = request.POST.get("estado", "Normal")
        power = request.POST.get("power", "POWER-ON")

        tarjeta = Tarjeta.objects.create(
            slot=slot,
            nombre=nombre,
            estado=estado,
            power=power
        )

        return JsonResponse({
            "id": tarjeta.id,
            "slot": tarjeta.slot,
            "nombre": tarjeta.nombre,
            "estado": tarjeta.estado,
            "power": tarjeta.power
        })
    return JsonResponse({"error": "Método no permitido"}, status=405)

@require_POST
def eliminar_tarjeta(request, pk):
    tarjeta = get_object_or_404(Tarjeta, pk=pk)
    tarjeta.delete()
    return JsonResponse({"success": True})
