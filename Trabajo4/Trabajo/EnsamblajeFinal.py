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
                print(f'Componente duplicado {component} {i} recibido en el tiempo {round(env.now)}. Ignorando...')
                continue  # Ignorar componentes duplicados
            components.append(component)
            print(f'{component} {i} llega a la línea de montaje en el tiempo {round(env.now)}')
        
        # Verificar que todos los componentes están presentes
        if set(components) == set(required_components):
            print(f'Comenzando el ensamblaje del ordenador {i} en el tiempo {round(env.now)}. Tiempo estimado: {len(components) * 2}')
            
            # Simular fallo aleatorio durante el ensamblaje 10% de probabilidad
            if random.random() < 0.1:
                print(f'FALLO El ensambale del ordenador {i} ha fallado. Reiniciando...')
                components.clear() # Vaciar componentes
                continue # Volver al inicio del bucle (sin incrementar i)
            
            # Si no hay fallo, comienza el ensamblaje
            yield env.timeout(random.uninform(len(components) * 2 - 1, len(components) * 2 + 1)) # Tiempo de ensamblaje dinámico
            print(f'Ordenador {i} ensamblado en el tiempo {round(env.now)}')
            i+=1
            
        else:
            print(f'Faltan componentes para el ensamblaje del ordenador {i} en el tiempo {round(env.now)}')
        
        components.clear()  # Reiniciar para el próximo ensamblaje
