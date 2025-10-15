from django.shortcuts import render, redirect

# Create your views here.


def index (request):
    return render(request, 'index.html', { 'menu': 0 })
# Punto de bienvenida al sitio

def welcome (request):
    return redirect('menu/select/0')

# Definie los primeros parametros de ingreso
def select (request, id):
    context= { }
    context['menu'] = id
    
    match id:
        case 0: # Bienvenida
            None
        case 1: # Paneles
            None
        case 2: # olt
            None
        case 3:
            None
        case 10: # Empresa
            None
    
    return render(request, 'index.html', context)