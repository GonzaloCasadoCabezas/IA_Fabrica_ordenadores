import random
from Transporte import transporte

def grafica(env, name, mf, assembly_time, going_main_time, components_store, transport_time):
    """
    Simula la fabricación y transporte de una gráfica.
    :param env: Entorno de simulación.
    :param name: Nombre de la gráfica.
    :param mf: Recurso de la fábrica principal.
    :param assembly_time: Tiempo de fabricación.
    :param going_main_time: Tiempo de ensamblaje en la fábrica principal.
    :param components_store: Almacén de componentes.
    :param transport_time: Tiempo de transporte a la fábrica principal.
    """
    max_reintentos = 3  # Límite de reintentos en caso de fallo
    reintentos = 0
    
    print(f'{name}: Llegan todos los componentes de la gráfica en el tiempo {round(env.now)}')

    while reintentos < max_reintentos:  # Reintentar en caso de fallo
        # Simular el tiempo de fabricación
        yield env.timeout(assembly_time)
        
        # Simular un fallo con un 10% de probabilidad
        if random.random() < 0.1:  # 10% de probabilidad de fallo
            print(f'{name}: Fallo en la fabricación. Reiniciando... (Intento {reintentos + 1})')
            reintentos += 1
            continue  # Reiniciar el proceso de fabricación
        
        # Si no hay fallo, continuar con el proceso
        break  # Salir del bucle si no hay fallo
    else:
        print(f'{name}: Fallo crítico. No se pudo fabricar la gráfica.')
        return  # Salir de la función si se supera el límite de reintentos

    
    
    # Pedir acceso a la fábrica principal
    
    with mf.request() as req:
        yield req
        
        # Simular el tiempo de ensamblaje en la fábrica principal
        print(f'{name}: Empieza la fabricación de la gráfica en el tiempo {round(env.now)}')
        yield env.timeout(going_main_time)
        print(f'{name}: Termina el ensamblaje en el tiempo {round(env.now)}')
        
        # Simular el transporte a la fábrica principal
        llegada = yield env.process(transporte(env, transport_time))
        retraso = llegada - env.now + transport_time  # Calcular el retraso
        print(f'{name}: Llegó a Fábrica Principal en el tiempo {llegada}(Retraso: {retraso:.2f})')
        
        # Enviar el componente al almacén
        yield components_store.put('Grafica')
        print(f'{name}: Gráfica enviada al almacén de componentes en el tiempo {round(env.now, 2)}')