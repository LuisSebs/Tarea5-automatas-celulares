import random

class Poblacion:

    """
        Simula una poblacion de Individuos en un
        algoritmo genetico para el problema de
        knapsack
    """

    class Individuo:

        """
            Simula un individuo de una poblacion
            en un algoritmo genetico para el 
            problema de knapsack
        """

        def __init__(self, cromosoma) -> None:
            self.cromosoma = cromosoma
            self.aptitud = None
        
        def mutacion(self):

            """
                Muta el cromosoma del individuo con una 
                probabilidad de 0.2 de ser mutado
            """

            n = len(self.cromosoma)
            probabilidad = 0.2
            # Recorremos el cromosoma del individuo
            for i in range(n):
                # Valor random entre [0,1]
                ran = random.random()
                if ran < probabilidad:
                    # Mutamos
                    self.cromosoma[i] = random.randint(0,1)
                    break

    def __init__(self,p=50, objetos=[random.randint(1,20) for _ in range(20)], m=50) -> None:
        """
            params:
                p: peso maximo de la mochila
                objetos: arreglo de los pesos de los objetos
                m: tamaño de la poblacion inicial
        """
        n = len(objetos) # Cantidad de objetos
        self.poblacion = [self.Individuo([random.randint(0,1) for _ in range(n)]) for _ in range(m)]
        self.peso_maximo = p
        self.objetos = objetos
        self.optimo = None # individuo optimo    

    def asignarAptitud(self):

        """
            Asigna a toda la poblacion
            la aptitud de los individuos
        """

        for i in self.poblacion:
            # Aptitud del individuo i
            ap = self.fitness(i.cromosoma)
            # Asignamos
            i.aptitud = ap
    
    def fitness(self,arr):

        """
            Regresa la aptitud del cromosoma, determina
            la aptitud del arreglo pasado como parametro. 
            Se basa en la cantidad de peso de la mochila.
            Cero es el valor optimo, mietras mas alejado 
            de cero sea el fitness menos optimo es.

            params: 
                arr: cromosoma del individuo
        """

        peso = 0

        for i in range(len(arr)):
            peso += self.objetos[i] if arr[i] == 1 else 0
        
        return abs(self.peso_maximo - peso)

    def elitismo(self):
        """
            Regresa al individuo con mejor aptitud.
            Adicionalmente asigna al mejor Individuo
            encontrado hasta el momento. (self.optimo)
        """

        # Mayor aptitud
        mayor = None
        # Indice del individuo
        indice = None

        for i in range(len(self.poblacion)):
            individuo = self.poblacion[i]
            if mayor == None  and indice == None:
                mayor = individuo.aptitud
                indice = i
            else:
                if individuo.aptitud <= mayor:
                    mayor = individuo.aptitud
                    indice = i
        
        # Asignamos al Individuo con mayor aptitud
        self.optimo = self.poblacion[indice]

        return self.optimo

    def seleccioRuleta(self):

        """
            Regresa a un Individuo de la poblacion
            en base a su % de supervivencia. Mientras
            mayor sea, mas probabilidades tiene de ser
            seleccionado
        """    

        sumatoria = 0

        # Sumatoria de todas las aptitudes de la poblacion
        for i in self.poblacion:
            sumatoria += i.aptitud

        # Individuo seleccionado
        individuo = None

        # Longitud de la poblacion
        n = len(self.poblacion)

        # Mientras no seleccionemos a un individuo
        while individuo == None:
            indice = random.randint(0,n-1)
            # Individuo aleatorio
            individuo_ran = self.poblacion[indice]
            # random in [0,1] | lo dividimos entre n para ajustar la probabilidad (si no nunca se elegira un individuo)
            ran = random.random()/n
            # Porcentaje de supervivencia (individuo_ran.aptitud/sumatoria)
            if ran > (individuo_ran.aptitud/sumatoria):
                individuo = self.poblacion[indice]

        return individuo

    def optimoEncontrado(self):
        """
            Regresa True si se ha encontrado al individuo 
            optimo, False en caso contrario.La aptitud 
            optima para el problema es 0
        """

        return False if self.optimo == None else self.optimo.aptitud == 0
    
def recombinacion(p1,p2):

    """
        Regresa un Individuo hijo resultado de la 
        mezcla de los cromosomas de ambos padres
    """

    n = len(p1.cromosoma)
    corte = random.randint(0,n-2)
    hijo = Poblacion().Individuo(p1.cromosoma[0:corte+1]+p2.cromosoma[corte+1:n])
    return hijo

if __name__ == "__main__":

    generaciones = 0

    poblacion = Poblacion()

    print(f"Peso maximo de la mochila: {poblacion.peso_maximo} ")
    print("Objetos y su peso: ")
    print(poblacion.objetos,"\n")

    poblacion.asignarAptitud()
    while generaciones < 1000 and (not poblacion.optimoEncontrado()):
        nuevaPoblacion = list()
        nuevaPoblacion.append(poblacion.elitismo())
        while len(nuevaPoblacion) < 50:
            individuo1 = poblacion.seleccioRuleta()
            individuo2 = poblacion.seleccioRuleta()
            hijo = recombinacion(individuo1, individuo2)
            hijo.mutacion()
            nuevaPoblacion.append(hijo)
        poblacion.poblacion = nuevaPoblacion
        poblacion.asignarAptitud()
        generaciones += 1
        # Cada 50 generaciones mostramos la mejor solucion
        if generaciones%50 == 0:
            print(f"Mejor solucion en iteracion {generaciones} es: \n{poblacion.optimo.cromosoma} \nfitness: {poblacion.optimo.aptitud}")

    # En caso de que hayamos encontrado al optimo
    if poblacion.optimoEncontrado():
        print(f"Se encontro el optimo en la generacion {generaciones}:")
        print(f"{poblacion.optimo.cromosoma}\nfitness: {poblacion.optimo.aptitud}",'\n')


    # Comprobacion:
    print("1: Llevar, 0: No llevar")
    peso_total_objetos = 0
    for i in range(len(poblacion.objetos)):
        objeto = poblacion.objetos[i]
        print(f"Objeto en la posicion {i}, peso: {objeto}, llevar?: {poblacion.optimo.cromosoma[i]}")
        if poblacion.optimo.cromosoma[i] == 1:
            peso_total_objetos += objeto
    
    print(f"Peso total de los objetos llevados: {peso_total_objetos}")

