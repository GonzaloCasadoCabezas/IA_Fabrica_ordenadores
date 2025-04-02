import simpy
import random
import pandas as pd
from datetime import datetime
random.seed(123)

# Import component manufacturing processes
from components.storage import storage
from components.box import box
from components.power_supply import power_supply
from components.ram import ram
from components.mother_board import mother_board
from components.processor import processor
from components.cooling_system import cooling_system
from components.graphics_card import graphics_card
from processes.final_assembly import final_assembly

simulation_results = []

def track_component_process(env, name, component_type, mf, assembly_time, main_assembly_time, 
                          components_store, transport_time):
    """
    Wrapper function to track component manufacturing process and collect data
    """
    start_time = env.now
    status = "Success"
    
    try:
        # Get the correct process function
        process_func = globals()[component_type.lower()]
        yield env.process(process_func(
            env, name, mf, assembly_time, main_assembly_time, 
            components_store, transport_time
        ))
    except Exception as e:
        status = f"Failed: {str(e)}"
    
    end_time = env.now
    total_time = end_time - start_time
    
    # Store results
    simulation_results.append({
        "Component": component_type,
        "Name": name,
        "Start_Time": start_time,
        "End_Time": end_time,
        "Total_Time": total_time,
        "Assembly_Time": assembly_time,
        "Main_Assembly_Time": main_assembly_time,
        "Transport_Time": transport_time,
        "Status": status
    })

if __name__ == '__main__':
    env = simpy.Environment()
    main_factory = simpy.Resource(env, capacity=1)
    components_store = simpy.Store(env)

    # Transportation times for each component
    transport_times = {
        'Processor': random.uniform(2, 5),  
        'GraphicsCard': random.uniform(3, 6),
        'Storage': random.uniform(2, 5),
        'Box': random.uniform(2, 3),
        'PowerSupply': random.uniform(2, 4),
        'RAM': random.uniform(3, 6),
        'Motherboard': random.uniform(4, 8),
        'CoolingSystem': random.uniform(2, 5)
    }
    
    # Component configuration
    components = {
        'Processor': processor,
        'GraphicsCard': graphics_card,
        'Storage': storage,
        'Box': box,
        'PowerSupply': power_supply,
        'RAM': ram,
        'Motherboard': mother_board,
        'CoolingSystem': cooling_system
    }
    
    # Create manufacturing processes USING THE TRACKING FUNCTION
    for component_type, process_func in components.items():
        for i in range(50):  # Reduced number for testing
            env.process(track_component_process(
                env, 
                f'{component_type}_{i}', 
                component_type,
                main_factory, 
                i, 
                round(random.uniform(2, 7)), 
                components_store, 
                round(transport_times[component_type])
            )
        )    

    # Start final assembly process
    env.process(final_assembly(env, main_factory, components_store))
    
    # Run the simulation
    env.run()
    
    # Verify data collection
    print(f"\nTotal de registros recolectados: {len(simulation_results)}")
    
    # Create DataFrame if we have data
    if simulation_results:
        df = pd.DataFrame(simulation_results)
        
        # Debug: show column names
        print("\nColumnas disponibles:", df.columns.tolist())
        
        # Calculate transport delay if possible
        required_cols = ['Transport_Time', 'End_Time', 'Start_Time', 
                        'Assembly_Time', 'Main_Assembly_Time']
        if all(col in df.columns for col in required_cols):
            df['Transport_Delay'] = df['Transport_Time'] - (
                df['End_Time'] - df['Start_Time'] - 
                df['Assembly_Time'] - df['Main_Assembly_Time']
            )
        
        # Save to CSV
        csv_filename = f"simulation_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(csv_filename, index=False)
        print(f"\nCSV generado correctamente: {csv_filename}")
        print("\nPrimeras filas:")
        print(df.head())
    else:
        print("\nError: No se recolectaron datos durante la simulación")
        print("Posibles causas:")
        print("1. Los procesos no llegaron a ejecutarse completamente")
        print("2. La función track_component_process no se llamó correctamente")
        print("3. La simulación terminó antes de recolectar datos")