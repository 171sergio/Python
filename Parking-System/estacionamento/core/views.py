from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Carro
from django.db.models import Avg
from datetime import timedelta


def index(request):
    return render(request, 'index.html')


def home(request):
    carros = Carro.objects.filter(saida__isnull=True)
    return render(request, 'home.html', {'carros': carros})


def entrada(request):
    erro = None
    if request.method == 'POST':
        placa = request.POST.get('placa')
        # Verifica se o carro já está no estacionamento (sem saída registrada)
        if Carro.objects.filter(placa=placa, saida__isnull=True).exists():
            erro = "Este carro já está no estacionamento."
        else:
            # Se não houver erro, registra a entrada
            Carro.objects.create(placa=placa)
            return redirect('home')
    
    # Retorna o erro (se houver) e o formulário de entrada
    return render(request, 'entrada.html', {'erro': erro})


def saida(request, carro_id):
    carro = get_object_or_404(Carro, id=carro_id)
    carro.saida = timezone.now()
    carro.save()
    
    # Obtenção de valores para mostrar o extrato de pagamento
    total_minutos = (carro.saida - carro.entrada).total_seconds() / 60
    total_horas = int(total_minutos // 60)
    total_minutos_restantes = int(total_minutos % 60)

    
    if total_minutos <= 10:
        valor_pago = 0.0
    else:
        if total_minutos % 60 > 0:
            total_horas += 1
        if total_horas <= 1:
            valor_pago = 5.0
        else:
            valor_pago = 5.0 + (total_horas - 1) * 2.0

    return render(request, 'saida.html', {
        'carro': carro,
        'total_horas': total_horas,
        'valor_pago': round(valor_pago, 2),
        'total_minutos_restantes': total_minutos_restantes,
        'total_minutos': total_minutos,
    })


def dashboard(request):
    agora = timezone.now()
    hoje_inicio = agora.replace(hour=0, minute=0, second=0, microsecond=0)

    carros_com_saida = Carro.objects.exclude(saida__isnull=True)
    total_carros = carros_com_saida.count()

    total_arrecadado = sum(c.valor_pago() for c in carros_com_saida)

    tempos = [
        (c.saida - c.entrada).total_seconds() / 60
        for c in carros_com_saida
        if c.saida and c.entrada
    ]
    
    media_tempo = sum(tempos) / len(tempos) if tempos else 0
    
    total_estacionados = Carro.objects.filter(saida__isnull=True).count()

    return render(request, 'dashboard.html', {
        'total_carros': total_carros,
        'total_arrecadado': round(total_arrecadado, 2),
        'media_tempo': round(media_tempo, 2),
        'total_entradas_hoje': total_entradas_hoje,
        'total_estacionados': total_estacionados,
    })
