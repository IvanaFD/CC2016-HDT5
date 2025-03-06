import simpy
import random

# Parámetros de simulación
RANDOM_SEED = 42
CANTIDAD_MEMORIA_RAM = 100
INTERVALO_ENTRADA = 10
INSTRUCCIONES_POR_CICLO = 3 
NUM_PROCESOS = 25

random.seed(RANDOM_SEED)

def run(env, nombre, memory_needed, instructions):
    llegada = env.now
    print(f"{nombre} llega en t={llegada:.2f}, necesita {memory_needed} de RAM y {instructions} instrucciones totales a realizar.")
    with.get(memory_needed) as req:
        yield req
        print(f"{nombre} obtiene RAM y pasa a Ready en t={env.now:.2f}")

def new(env, nombre, ram, cpu, memory_needed, instructions):
    with ram.get(memory_needed) as req:
        yield req
        print(f"{nombre} obtiene {memory_needed} de RAM y pasa a Ready en t={env.now:.2f}")
        yield env.process(ready(env, nombre, ram, cpu, memory_needed, instructions))

def ready(env, nombre, ram, cpu, memory_needed, instructions):
    with cpu.request() as req:
        yield req
        print(f"{nombre} pasa a Running en t={env.now:.2f}")
        yield env.process(running(env, nombre, ram, cpu, memory_needed, instructions))

def running(env, nombre, ram, cpu, memory_needed, instructions):
    yield env.timeout(1)
    instructions -= INSTRUCCIONES_POR_CICLO
    print(f"{env.now:.2f} - {nombre} ejecuta en Running, restan {max(instructions, 0)} instrucciones.")
    
    if instructions <= 0:
        yield env.process(terminated(env, nombre, ram, memory_needed))
    else:
        decision = random.randint(1, 2)
        if decision == 1:
            yield env.process(waiting(env, nombre, ram, cpu, memory_needed, instructions))
        else:
            yield env.process(ready(env, nombre, ram, cpu, memory_needed, instructions))

def waiting(env, nombre, ram, cpu, memory_needed, instructions):
    print(f"{nombre} pasa a Waiting en t={env.now:.2f}")
    yield env.timeout(random.randint(1, 2))
    print(f"{nombre} vuelve a Ready desde Waiting en t={env.now:.2f}")
    yield env.process(ready(env, nombre, ram, cpu, memory_needed, instructions))

def terminated(env, nombre, ram, memory_needed):
    print(f"{nombre} termina en t={env.now:.2f} y libera {memory_needed} de RAM")
    yield ram.put(memory_needed)

def create(env, num_procesos, ram, cpu):
    for i in range(num_procesos):
        yield env.timeout(random.expovariate(1.0 / INTERVALO_ENTRADA))
        env.process(run(env, f'Proceso {i+1}', ram, cpu)) 

# Configuración de simulación
env = simpy.Environment()
ram = simpy.Container(env, init=CANTIDAD_MEMORIA_RAM, capacity=CANTIDAD_MEMORIA_RAM)
cpu = simpy.Resource(env, capacity=1)

env.process(create(env, NUM_PROCESOS, ram, cpu))

env.run()