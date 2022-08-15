"""
-------------------------------------------
Author : Sobhan Shukueian
Project : TSP with genetic alogorithms
-------------------------------------------
"""


import math,random,numpy
import matplotlib.pyplot as plt
class City:
    """
    City objects class to define cities with x and y coordinates
    """
    def __init__(self,x,y):
        self.x = x
        self.y = y
    
    def Distance(self,other):
        return math.sqrt(((self.x - other.x) ** 2) + ((self.y - other.y) ** 2))
    
    def GetX(self):
        return self.x

    def GetY(self):
        return self.y

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")"

choromosome = [City(37 ,52), City(49 ,49), City(52 ,64), City(20 ,26), City(40 ,30), City(21 ,7), City(17 ,63), City(31 ,62), City(52 ,33), City(51 ,21), City(42 ,41), City(31 ,32), City(5 ,25) , City(12 ,42), City(36 ,16), City(52 ,41), City(27, 23), City(17,33), City(13 ,13) , City(57 ,58), City(62 ,42), City(42,57), City(16 ,57), City(8 ,52), City(7 ,38),  City(27 ,68), City(30 ,48), City(43 ,67),City(58 ,48),City(58 ,27),City(37,69),City(38 ,46),City(46 ,10), City(61 ,33),City(62 ,63),City(63 ,69),City(32 ,22),City(45 ,35),City(59 ,15),City(5 ,6),City(10 ,17),City(21 ,10), City(5 ,64)  ,City(30 ,15),City(39 ,10),City(32 ,39),City(25 ,32), City(25 ,55), City(48 ,28), City(56 ,37), City(30 ,40)]

def CreatePopulation(choromosome, popSize):
    """ Population genrator function

    Args:
        choromosome (City): choromosome list
        popSize (int): population size

    Returns:
        array: population list
    """
    population = []
    for i in range(popSize):
        population.append(random.sample(choromosome,len(choromosome)))
    return population

def TotalDistance(choromosome):
    """Calculate total distance of cities in a chromosome

    Args:
        choromosome (array): _description_

    Returns:
        int: total distance
    """
    total_distance = 0
    for i in range(len(choromosome)):
        source = choromosome[i]
        if i + 1 < len(choromosome):
            destination = choromosome[i + 1]
        else:
            destination = choromosome[0]
        total_distance += source.Distance(destination)
    return total_distance 

def Fitness(population):
    """Fitness calculator

    Args:
        population (array): population

    Returns:
        dict: fitness
    """
    fitness = {}
    for i in range(len(population)):
        fitness[tuple(population[i])] = (1 / TotalDistance(population[i]))
    return fitness

def Probabilities(fitness):
    """Probabilities calculator

    Args:
        fitness (dict): fintness dict

    Returns:
        array: probabilities
    """
    fitnesses = fitness.values()
    total_fit = float(sum(fitnesses))
    relative_fitness = [f/total_fit for f in fitnesses]
    probabilities = [sum(relative_fitness[:i+1]) 
                     for i in range(len(relative_fitness))]
    return probabilities

def RouletteWheel(population, probabilities, number):
    chosen = []
    for n in range(number):
        r = random.random()
        for (i, roulette_wheel) in enumerate(population):
            if r <= probabilities[i]:
                chosen.append(list(roulette_wheel))
                break
    return chosen

def OnePointCrossover(roulette_wheel):
    """One point crossover

    Args:
        roulette_wheel (array): roulette wheel array

    Returns:
        array: one point crossover
    """
    crossover = []
    i = 0
    while i < len(roulette_wheel) - 1:
        child1 = []
        child2 = []
        child1 += roulette_wheel[i][:5]
        child1 += roulette_wheel[i+1][5:]
        child2 += roulette_wheel[i+1][:5]
        child2 += roulette_wheel[i][5:]
        x = [item for item in roulette_wheel[0] if item not in child1]        
        child1 += x
        child1 = list(dict.fromkeys(child1))
        x = [item for item in roulette_wheel[0] if item not in child2]
        child2 += x
        child2 = list(dict.fromkeys(child2))
        crossover.append(child1)
        crossover.append(child2)
        i += 2
    return crossover

def TwoPointCrossover(roulette_wheel):
    """Two point crossover

    Args:
        roulette_wheel (array): roulette wheel array

    Returns:
        array: two point crossover
    """
    crossover = []
    j = 0
    while j < len(roulette_wheel) - 1:
        child1 = []
        child2 = []
        i = 0
        while i < len(roulette_wheel[0])  :
            parent1 = roulette_wheel[j][i]
            parent2 = roulette_wheel[j + 1][i]
            if i < 0.25 * len(roulette_wheel[0]):
                child1.append(parent1)
                child2.append(parent2)
            elif i < 0.5 * len(roulette_wheel[0]):
                child2.append(parent1)
                child1.append(parent2)
            elif i < 0.75 * len(roulette_wheel[0]):
                child2.append(parent1)
                child1.append(parent2)
            elif i < len(roulette_wheel[0]):
                child1.append(parent1)
                child2.append(parent2)
            i += 1
        x = [item for item in roulette_wheel[0] if item not in child1]        
        child1 += x
        child1 = list(dict.fromkeys(child1))
        x = [item for item in roulette_wheel[0] if item not in child2]
        child2 += x
        child2 = list(dict.fromkeys(child2))
        crossover.append(child1)        
        crossover.append(child2)
        j += 2
    return crossover

def Mutation(roulette_wheel, mutate_rate):
    """Randomly mutate population

    Args:
        roulette_wheel (array): roulette wheel output
        mutate_rate (float): Mutate Rate

    Returns:
        array: Mutation 
    """
    mutation = []
    for i in roulette_wheel:
        for swapped in range(len(roulette_wheel)):
            if(random.random() < mutate_rate):
                swapWith = int(random.random() * len(roulette_wheel))
                
                city1 = roulette_wheel[swapped]
                city2 = roulette_wheel[swapWith]
                
                roulette_wheel[swapped] = city2
                roulette_wheel[swapWith] = city1
        mutation.append(i)
    return mutation

def GetBest(generations):
    routes = {}
    for i in generations:
        routes[tuple(i)] = (TotalDistance(i))
    return routes


def Draw(min_index):
    X = []
    Y = []
    for city in min_index:
        X.append(city.GetX())
        Y.append(city.GetY())
    plt.title("The travelling salesman problem")
    plt.plot(X,Y)
    plt.xlabel = ("X")
    plt.ylabel = ("Y")
    plt.show()


def main(choromosome, loop):
    """Main function
    """
    best = {}
    for i in range(loop):
        population = CreatePopulation(choromosome, 100)
        fitness = Fitness(population)
        probability_list = Probabilities(fitness)
        roulette_wheel = RouletteWheel(population, probability_list,30)
        one_point_crossover = OnePointCrossover(roulette_wheel)
        two_point_crossover = TwoPointCrossover(roulette_wheel)
        mutation = Mutation(roulette_wheel,0.01)
        generations = roulette_wheel + one_point_crossover + mutation + two_point_crossover 
        best.update(GetBest(generations))
    min_index = min(best.keys(), key=(lambda k: best[k]))
    print("The Best City Arrange => ", list(min_index))
    print("The Best Route =>" , best[min_index])
    return min_index

if __name__ == '__main__':  
    print("Cities coordinates => " , choromosome)
    min_index = main(choromosome,500)
    Draw(min_index)