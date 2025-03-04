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
    def _init_(self, env, nombre, ram, cpu, stats): 
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

    def new(self):
        #Solicita la ram que va utilizar sino hace la espera en la cola hasta que se libere ram para utilizar
        with self.ram.get(self.memory_needed) as req:
            yield req
            print(f"{self.name} obtiene {self.memory_needed} de RAM y pasa a Ready en t={self.env.now:.2f}")
            yield self.env.process(self.ready())  #Obtiene la ram y pasa a la cola de ready

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
        print(f"{self.name} pasa a Running en t={self.env.now:.2f}")

        if self.instructions <= INSTRUCCIONES_POR_CICLO:
            yield self.env.process(terminated(self))
        else: 
            decision = random.randint(1, 2)
            if decision == 1:
                yield self.env.process(self.ready())
            else:
                yield self.env.process(self.waiting())




