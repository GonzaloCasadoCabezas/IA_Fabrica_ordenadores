import random

def transporte(env, transport_time):
    """
    Simula el transporte de un componente con posibles retrasos aleatorios.
    :param env: Entorno de simulación.
    :param transport_time: Tiempo base de transporte.
    :return: Tiempo de llegada redondeado a 2 decimales.
    """
    # Generar un retraso aleatorio entre 0 y 2 unidades de tiempo
    retraso = random.uniform(0, 2)  # Retraso aleatorio entre 0 y 2
    tiempo_total = transport_time + retraso  # Tiempo de transporte con retraso
    
    # Simular el tiempo de transporte
    yield env.timeout(tiempo_total)
    
    # Devolver el tiempo de llegada redondeado a 2 decimales
    return round(env.now, 2)