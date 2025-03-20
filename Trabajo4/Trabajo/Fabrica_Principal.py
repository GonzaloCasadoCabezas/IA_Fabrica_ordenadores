import simpy

#nos traemos la funcion procesador y grafica de sus respectivos ficheros
from Almacenamiento import almacenamiento
from Caja import caja
from FuenteDeAlimentacion import alimentacion
from MemoriaRam import ram
from PlacaBase import base
from Procesador import procesador
from SistemaDeRefrigeracion import refrigeracion
from Tarjeta_Grafica import grafica

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

if __name__=='__main__':
    env = simpy.Environment()
    mf = simpy.Resource(env, capacity=1)
    # Store es una clase de la libreria simpy para almacenar objetos lo usamos para almacenar los componentes y saber si estan
    components_store = simpy.Store(env)

    # Tiempos de transporte para cada componente
    transport_times = {
        'Procesador': 2,
        'Grafica': 3,
        'Almacenamiento': 4,
        'Caja': 1,
        'FuenteDeAlimentacion': 2,
        'MemoriaRam': 3,
        'PlacaBase': 4,
        'SistemaDeRefrigeracion': 2
    }
    
    env.process(ensamblaje_final(env, mf, components_store))
    #mirar esto
    for i in range(4):
        env.process(procesador(env, f'Procesador {i}', mf, i, 5, 
                               components_store, transport_times['Procesador']))   
    for i in range(4):
        env.process(grafica(env, f'Grafica {i}', mf, i, 3,
                            components_store, transport_times['Grafica']))        
    for i in range(4):
        env.process(almacenamiento(env, f'Almacenamiento {i}', mf, i, 4,
                                   components_store, transport_times['Almacenamiento']))
    for i in range(4):
        env.process(caja(env, f'Caja {i}', mf, i, 2,
                         components_store, transport_times['Caja']))
    for i in range(4):
        env.process(alimentacion(env, f'FuenteDeAlimentacion {i}', mf, i, 3,
                                 components_store, transport_times['FuenteDeAlimentacion']))
    for i in range(4):
        env.process(ram(env, f'MemoriaRam {i}', mf, i, 3,
                        components_store, transport_times['MemoriaRam']))
    for i in range(4):
        env.process(base(env, f'PlacaBase {i}', mf, i, 4,
                         components_store, transport_times['PlacaBase']))
    for i in range(4):
        env.process(refrigeracion(env, f'SistemaDeRefrigeracion {i}', mf, i, 3,
                                  components_store, transport_times['SistemaDeRefrigeracion']))

    env.run()  