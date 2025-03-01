import simpy
import random

#Parametros de simulación
#RANDOM_SEED = 42
CANTIDAD_MEMORIA_RAM = 100
INTERVALO_ENTRADA = 10
INSTRUCCIONES_POR_CICLO = 3 
NUM_PROCESOS = 25
INTERVALO_DE_EJECUCION = 1


#Constructor de un proceso con sus datos iniciales de ram requerida e instrucciones que va realizar
def proceso(self, env, nombre, ram, cpu, stats): 
    self.env = env
    self.name = nombre
    self.ram = ram
    self.cpu = cpu
    self.instructions = random.randint(1, 10)
    self.memory_needed = random.randint(1, 10)
    self.start_time = env.now
    self.stats = stats
    print(f"{self.name} llega al sistema (requiere {self.memory_needed} de RAM) en t={self.env.now:.2f}")
    env.process(self.new()) 

