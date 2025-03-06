
#  Universidad del Valle de Guatemala
#  Algoritmos y Estructuras de Datos - Sección 31
#  Hoja de Trabajo 5
#  Integrantes:
#  Diana Sosa 241040
#  Biancka Raxón 24960
#  Ivana Figueroa 24785
 


# Referencias: 
# - https://www.youtube.com/watch?v=BqZxmbhJ14Q

import simpy
import random
import numpy as np

# Parámetros de simulación
RANDOM_SEED = 42
CANTIDAD_MEMORIA_RAM = 2
INSTRUCCIONES_POR_CICLO = 3 #Instrucciones por ciclo que ejecutará el CPU
INTERVALO_ENTRADA = 1  # Intervalo de llegada de los procesos
NUMERO_PRCESOS = 200  # Numero de procesos a simular

random.seed(RANDOM_SEED)

def proceso(env, nombre, ram, cpu, memory_needed, instructions, tiempos):
    tiempo_llegada = env.now
    print(f"{nombre} llega, necesita {memory_needed} de RAM y tiene {instructions} instrucciones a realizar.")
    
    with ram.get(memory_needed) as req_ram:
        yield req_ram
        print(f"{nombre} obtiene RAM y pasa a Ready.")
        
        with cpu.request() as req_cpu:
            yield req_cpu
            print(f"{nombre} pasa a Running y comienza su ejecución.")
            
            while instructions > 0:
                yield env.timeout(1)
                instructions -= INSTRUCCIONES_POR_CICLO
                print(f"{nombre} ejecutó en Running, le quedan {max(instructions, 0)} instrucciones pendientes.")
                
                if instructions > 0:
                    decision = random.randint(1, 2)
                    if decision == 1:
                        print(f"{nombre} vuelve a Ready.")
                    else:
                        print(f"{nombre} pasa a Waiting.")
                        yield env.timeout(random.randint(1, 2))
                        print(f"{nombre} vuelve a Ready.")
            ram.put(memory_needed)
    
    tiempo_total = env.now - tiempo_llegada
    tiempos.append(tiempo_total)
    #print(f"{nombre} terminó en {env.now:.2f} s, tiempo total en sistema: {tiempo_total:.2f}")
    print(f"{nombre} estuvo en el sistema un tiempo total de {tiempo_total:.2f} s.")


def generador_procesos(env, num_procesos, intervalo, ram, cpu, tiempos):
    for i in range(num_procesos):
        yield env.timeout(random.expovariate(1.0 / intervalo))
        memory_needed = random.randint(1, 10)
        instructions = random.randint(1, 10)
        env.process(proceso(env, f'Proceso {i+1}', ram, cpu, memory_needed, instructions, tiempos))

def simular(intervalo, num_procesos):
    env = simpy.Environment()
    ram = simpy.Container(env, init=CANTIDAD_MEMORIA_RAM, capacity=CANTIDAD_MEMORIA_RAM)
    cpu = simpy.Resource(env, capacity=1)
    tiempos = []
    env.process(generador_procesos(env, num_procesos, intervalo, ram, cpu, tiempos))
    env.run()
    print(f"Simulación con {num_procesos} procesos e intervalo de {intervalo}: \n - Tiempo promedio = {np.mean(tiempos):.2f} s \n - Desviación estándar = {np.std(tiempos):.2f} s")

# Iniciar la simulacion
simular(INTERVALO_ENTRADA, NUMERO_PRCESOS)
