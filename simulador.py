import simpy
import random

#Parametros de simulación
#RANDOM_SEED = 42
CANTIDAD_MEMORIA_RAM = 100
INTERVALO_ENTRADA = 10
INSTRUCCIONES_POR_CICLO = 3 
NUM_PROCESOS = 25
INTERVALO_DE_EJECUCION = 1

def run(env, nombre, ram, cpu):
    instructions = random.radiant(1,10)
    memory_needed = random.radiant(1,10)
    start_time = env.now
    print(f"{nombre} llega al sistema decesita {memory_needed} de RAM en t= {env.now:.2f})")
    yield env.process(new(env,nombre,ram,cpu,memory_needed,instructions))


def new(env, nombre, ram, cpu, memory_needed, instructions):
    with ram.get(memory_needed) as req:
        yield req
        print(f"{nombre} obtine {memory_needed} de RAM y pasa a ready en t= {env.now:.2f})")
        yield env.process(ready(env,nombre,ram,cpu,memory_needed, instructions))

   
def ready(env, nombre, ram, cpu, memory_needed, instructions):
    print(f"{nombre} pasa a ready en t= {env.now:.2f})")
    while instructions > 0:
        with cpu.request() as req:
            yield req
            print(f"{nombre} pasa a running en t= {env.now:.2f})")
            instructions = yield env.process(running(env,nombre,ram,cpu,memory_needed, instructions))


    

#Proceso ejecutandose en el CPU
def running(env, nombre, ram, cpu, memory_needed, instructions):
    yield env.timeout(1)
    instructions -= INSTRUCCIONES_POR_CICLO
    print(f"{env.now:.2f} - {nombre} pasa a Running en t={env.now:.2f}, faltan {max(instructions, 0)} instrucciones.")
    if instructions <= 0:
        yield env.process(terminated(env, nombre, ram, memory_needed))
    else:
        decision = random.randint(1, 2)
        if decision == 1:
            yield env.process(ready(env, nombre, ram, cpu, memory_needed, instructions))
        else:
            yield env.process(waiting(env, nombre, ram, cpu, memory_needed, instructions))



def waiting(self):
    print(f"{self.name} pasa a waiting en t={self.env.now:.2f}")
    yield self.env.timeout(random.randint(1, 2))
    print(f"{self.name} vuelve a Ready desde Waiting en t={self.env.now:.2f}")
    yield self.env.process(self.ready())

def terminated(self):
    #Proceso termina y libera la RAM que estaba usando
    print(f"{self.name} termina en t={self.env.now:.2f}")
    self.ram.put(self.memory_needed)

def create(env, num_procesos, ram, cpu):
    for i in range(num_procesos):
        yield env.timeout(random.expovariate(1.0 / INTERVALO_ENTRADA))  # Genera procesos en intervalos aleatorios
        env.process(run(env, f'Proceso-{i+1}', ram, cpu)) 

#Configuracion simulacion
env = simpy.Environment()
ram = simpy.Container(env, capacity=1000, init=1000)  # Configura la memoria
cpu = simpy.Resource(env, capacity=1)  # Configura solo un CPU

#Inicia la creacion de procesos
env.process(create(env, NUM_PROCESOS, ram, cpu))

#Iniciar la simulación
env.run()


