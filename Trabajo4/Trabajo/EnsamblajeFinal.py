import random
import simpy

def ensamblaje_final(env, mf, components_store):
    required_components = ['Procesador', 'Grafica', 'Almacenamiento', 
                           'Caja', 'FuenteDeAlimentacion', 'MemoriaRam', 'PlacaBase', 'SistemaDeRefrigeracion']
    
    while True:
        components = []
        while len(components) < len(required_components):
            component = yield components_store.get()
            if component in components:
                print(f'Componente duplicado {component} recibido en el tiempo {round(env.now)}. Ignorando...')
                continue  # Ignorar componentes duplicados
            components.append(component)
            print(f'{component} llega a la línea de montaje en el tiempo {round(env.now)}')
        
        # Verificar que todos los componentes están presentes
        if set(components) == set(required_components):
            print(f'Comenzando el ensamblaje en el tiempo {round(env.now)}. Tiempo estimado: {len(components) * 2}')
            yield env.timeout(len(components) * 2)  # Tiempo de ensamblaje dinámico
            print(f'Ordenador ensamblado en el tiempo {round(env.now)}')
        else:
            print(f'Faltan componentes para el ensamblaje en el tiempo {round(env.now)}')
        
        components.clear()  # Reiniciar para el próximo ensamblaje