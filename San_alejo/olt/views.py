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
    
def detalle_tarjeta(request, tarjeta_id):
    tarjeta = get_object_or_404(Tarjeta, id=tarjeta_id)
    puertos = tarjeta.puertos.all()
    onts = ONT.objects.filter(puerto__tarjeta=tarjeta)
    
    return render(request, 'detalle_tarjeta.html', {'tarjeta': tarjeta, 'puertos': puertos, 'onts': onts})

def agregar_puerto(request, tarjeta_id):
    if request.method == 'POST':
        tarjeta = get_object_or_404(Tarjeta, id=tarjeta_id)
        numero = request.POST.get('numero', 0)
        port = request.POST.get('port')
        tipo = request.POST.get('tipo')
        min_distance = request.POST.get('min_distance') or 0
        max_distance = request.POST.get('max_distance') or 0
        status = request.POST.get('status', 'Offline')

        puerto = Puerto.objects.create(
            tarjeta=tarjeta,
            numero=numero,
            port=port,
            tipo=tipo,
            min_distance=min_distance,
            max_distance=max_distance,
            status=status
        )
        return JsonResponse({
            'id': puerto.id,
            'numero': puerto.numero,
            'port': puerto.port,
            'tipo': puerto.tipo,
            'min_distance': str(puerto.min_distance),
            'max_distance': str(puerto.max_distance),
            'status': puerto.status
        })
    return JsonResponse({'error': 'Método no permitido'}, status=400)

def agregar_ont(request, puerto_id):
    if request.method == "POST":
        puerto = get_object_or_404(Puerto, id=puerto_id)
        nombre = request.POST.get("nombre_ont")
        sn = request.POST.get("sn")
        control_flag = request.POST.get("control_flag", "active")

        ont = ONT(puerto=puerto, nombre=nombre, sn=sn, control_flag=control_flag)
        ont.save()

        return JsonResponse({
            "ont_id": ont.ont_id,
            "service_port": ont.service_port,
            "nombre": ont.nombre,
            "sn": ont.sn,
            "control_flag": ont.control_flag,
            "run_state": ont.run_state,
            "config_state": ont.config_state,
            "match_state": ont.match_state,
            "fsp": f"{puerto.port}"
        })

    return JsonResponse({"error": "Método no permitido"}, status=400)

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
