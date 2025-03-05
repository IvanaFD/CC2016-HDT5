import simpy
import random

#Parametros de simulación
#RANDOM_SEED = 42
CANTIDAD_MEMORIA_RAM = 100
INTERVALO_ENTRADA = 10
INSTRUCCIONES_POR_CICLO = 3 
NUM_PROCESOS = 25
INTERVALO_DE_EJECUCION = 1

 

class Proceso:
    #Constructor de un proceso con sus datos iniciales de ram requerida e instrucciones que va realizar
    def __init__(self, env, nombre, ram, cpu, stats): 
        self.env = env
        self.name = nombre
        self.ram = ram
        self.cpu = cpu
        self.instructions = random.randint(1, 10)
        self.memory_needed = random.randint(1, 10)
        self.start_time = env.now
        print(f"{self.name} llega al sistema (requiere {self.memory_needed} de RAM) en t={self.env.now:.2f}")
        env.process(self.new()) 


def new(env, nombre, ram, cpu, memory_needed, instructions):
    with ram.get(memory_needed) as req:
        yield req
        print(f"{nombre} obtine {memory_needed} de RAM y pasa a ready en t= {env.now:.2f})")
        yield env.process(ready(env,nombre,ram,cpu,memory_needed, instructions))

   
def ready(self):
        #Pasa a la cola de ready
        print(f"{self.name} pasa a Rrady en t={self.env.now:.2f}")
        while self.instructions > 0:
            #Hace la espera del CPU si esta ocupado para luego realizar sus intrucciones
            with self.cpu.request() as req:
                yield req
                print(f"{self.name} pasa a Running en t={self.env.now:.2f}")
                yield self.env.process(self.running())  # Una vez tenga el CPU espacio pasa a Running

#Proceso ejecutandose en el CPU
def running(self):
    yield self.env.timeout(1)
    self.instructions -= INSTRUCCIONES_POR_CICLO
    print(f"{self.env.now:.2f} - {self.name} pasa a Running en t={self.env.now:.2f}, faltan {max(self.instructions - INSTRUCCIONES_POR_CICLO, 0)} isntrucciones. ")

    if self.instructions <= 0:
        yield self.env.process(self.terminated())
    else: 
        decision = random.randint(1, 2)
        if decision == 1:
            yield self.env.process(self.ready())
        else:
            yield self.env.process(self.waiting())

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
        env.process(Proceso(env, f'Proceso-{i+1}', ram, cpu).run()) 

#Configuracion simulacion
env = simpy.Environment()
ram = simpy.Container(env, capacity=1000, init=1000)  # Configura la memoria
cpu = simpy.Resource(env, capacity=1)  # Configura solo un CPU

#Inicia la creacion de procesos
env.process(create(env, NUM_PROCESOS, ram, cpu))

#Iniciar la simulación
env.run()


