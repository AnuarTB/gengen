import copy
import random
import time


class Input(object):
    def __init__(self, input_args, input_kwargs, fitness=None):
        self.input_args = input_args
        self.input_kwargs = input_kwargs
        self.fitness = None

    def crossover(self, other):
        tmp_args = list()
        tmp_kwargs = dict()
        for i in range(len(self.input_args)):
            tmp_args.append(self.input_args[i].crossover(other.input_args[i]))

        for k in self.input_kwargs.keys():
            tmp_kwargs[k] = self.input_kwargs[k].crossover(other.input_kwargs[k])

        return self.__class__(tmp_args, tmp_kwargs)

    def mutation(self):
        tmp_args = list()
        tmp_kwargs = dict()
        for i in range(len(self.input_args)):
            tmp_args.append(self.input_args[i].mutation())

        for k in self.input_kwargs.keys():
            tmp_kwargs[k] = self.input_kwargs[k].mutation()

        return self.__class__(tmp_args, tmp_kwargs)

    def generate(self):
        '''
        Returns the values in the form of tuple (args, kwargs) where:
        args - generated positional arguments
        kwargs - generated keyword arguments
        '''
        tmp_args = list()
        tmp_kwargs = dict()
        for i in range(len(self.input_args)):
            tmp_args.append(self.input_args[i].generate())

        for k in self.input_kwargs.keys():
            tmp_kwargs[k] = self.input_kwargs[k].generate()

        return tmp_args, tmp_kwargs

    def calc_fitness(self, func):
        if not self.fitness:
            args, kwargs = self.generate()
            start_time = time.time()
            func(*args, **kwargs)
            self.fitness = time.time() - start_time
        return self.fitness

class EvoGen(object):
    def __init__(self, initNum=100, iterNum=300):
        self.initNum = initNum  # The initial population number
        self.iterNum = iterNum # The number of generations
        self.input_class = None

    def createInput(self):
        return copy.deepcopy(self.input_class)

    def select(self, population):
        #TODO(@anuartb) Write this function properly
        return population[random.randint(0, 10)]

    def generateWorstCase(self, func, *args, **kwargs):
        self.input_class = Input(args, kwargs)
        population = []
        for _ in range(self.initNum):
            population.append(self.createInput())

        population.sort(key=lambda x: -x.calc_fitness(func))

        fittest = population[0]

        for it in range(self.iterNum):
            new_population = []
            for _ in range(self.initNum):
                a = self.select(population)
                b = self.select(population)
                c = a.crossover(b)
                if random.random() > 0.8:
                    c = c.mutation()
                new_population.append(c)
            population = new_population
            population.sort(key=lambda x: -x.calc_fitness(func))
            if population[0].calc_fitness(func) > fittest.calc_fitness(func):
                fittest = population[0]

            print('Generation #{}, fittest gene metrics: {}'.format(
                it, population[0].calc_fitness(func)))

        return fittest.generate(), fittest.calc_fitness(func)