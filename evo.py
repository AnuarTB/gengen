import bisect
import copy
import random
import time

import generic


class Input(object):
    def __init__(self, input_args, input_kwargs, fitness=None):
        """
        A simple wrapper object for the function arguments
        where input_args and input_kwargs are *args and **kwargs
        respectively.

        fitness is the current fitness of the Input instance. If it is
        not calculated, it will be calculated and the result will be
        memorized.
        """
        self.input_args = input_args
        self.input_kwargs = input_kwargs
        self.fitness = fitness

    def crossover(self, other):
        tmp_args = []
        tmp_kwargs = {}

        for i in range(len(self.input_args)):
            tmp_args.append(self.input_args[i].crossover(
                other.input_args[i]))

        for k in self.input_kwargs.keys():
            tmp_kwargs[k] = self.input_kwargs[k].crossover(
                other.input_kwargs[k])

        return self.__class__(tmp_args, tmp_kwargs)

    def _mutation(self, c, mutator_int, mutator_float, mutator_string, 
                  mutator_list, mutator_tuple, mutator_dict):
        if isinstance(c, generic.Int):
            c = c.mutation(mutator_int)
        elif isinstance(c, generic.Float):
            c = c.mutation(mutator_float)
        elif isinstance(c, generic.String):
            c = c.mutation(mutator_string)
        elif isinstance(c, generic.List):
            c = c.mutation(mutator_list)
        elif isinstance(c, generic.Tuple):
            c = c.mutation(mutator_tuple)
        elif isinstance(c, generic.Dict):
            c = c.mutation(mutator_dict)
        return c

    def mutation(self, mutator_int, mutator_float, mutator_string, 
                 mutator_list, mutator_tuple, mutator_dict):
        tmp_args = []
        tmp_kwargs = {}

        for i in range(len(self.input_args)):
            tmp_args.append(self._mutation(self.input_args[i], 
                                      mutator_int, mutator_float, mutator_string, 
                                      mutator_list, mutator_tuple, mutator_dict))

        for k in self.input_kwargs.keys():
            tmp_kwargs[k] = self._mutation(self.input_kwargs[k], 
                                      mutator_int, mutator_float, mutator_string, 
                                      mutator_list, mutator_tuple, mutator_dict)

        return self.__class__(tmp_args, tmp_kwargs)

    def generate(self):
        """
        Returns the values in the form of tuple (args, kwargs) where:
            args - generated positional arguments
            kwargs - generated keyword arguments
        """
        tmp_args = []
        tmp_kwargs = {}

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
    def __init__(self, pop_num=100, iter_num=300, mut_prob=0.2, parent_selection=0, ratio=0.2, 
                 mutator_int=0, mutator_float=0, mutator_string=0, 
                 mutator_list=0, mutator_tuple=0, mutator_dict=0):
        """
        In order to generate the worst input for the function, this
        wrapper class is instantiated with some of the hyperparameters
        listed below.
        """
        self.pop_num = pop_num  # The population number
        self.iter_num = iter_num  # The number of generations
        self.mut_prob = mut_prob  # The probability that the input will mutate
        self.parent_selection = parent_selection  # parent selection strategy number
        self.ratio = ratio  # what ratio of old populatio should we preserve
        
        self.mutator_int = mutator_int
        self.mutator_float = mutator_float
        self.mutator_string = mutator_string
        self.mutator_list = mutator_list
        self.mutator_tuple = mutator_tuple
        self.mutator_dict = mutator_dict

        self.input_class = None

    def create_input(self):
        return copy.deepcopy(self.input_class)

    def select(self, population, fitnesses, r):
        index = bisect.bisect_left(fitnesses, r)
        return population[index - 1 if index == len(fitnesses) else index]

    def generate_worst_case(self, func, *args, **kwargs):
        """
        Returns the worst input in terms of some predefined metrics
        (default: time) for the function 'func'.

        The first argument of this method is 'func' - function under test.
        Next are the arguments of the 'func', in the order they are placed in
        'func'.

        NOTE: Keyword arguments are also supported.
        """
        self.input_class = Input(args, kwargs)

        population = []
        for _ in range(self.pop_num):
            population.append(self.create_input())

        population.sort(key=lambda x: -x.calc_fitness(func))

        fittest = population[0]
        for it in range(self.iter_num):
            new_population = []

            fitnesses = []
            sum_fitnesses = 0
            for osob in population:
                fitness = osob.calc_fitness(func)
                fitnesses.append(fitness)
                sum_fitnesses += fitness

            for i in range(len(fitnesses)):
                fitnesses[i] /= sum_fitnesses
                if i > 0:
                    fitnesses[i] += fitnesses[i - 1]
            
            for _ in range(self.pop_num):
                a = self.select(population, fitnesses, random.random())
                b = self.select(population, fitnesses, random.random())
                c = a.crossover(b)

                if random.random() < self.mut_prob:
                    c = c.mutation(self.mutator_int, self.mutator_float, self.mutator_string,
                                   self.mutator_list, self.mutator_tuple, self.mutator_dict)
                    
                new_population.append(c)

            new_population.sort(key=lambda x: -x.calc_fitness(func))
            
            if self.parent_selection == 0:
                population += new_population
            elif self.parent_selection == 1:
                population = population[:int(self.ratio * self.pop_num) + 1] + new_population[:int((1.0 - self.ratio) * self.pop_num) + 1]
            else:
                population = new_population
            
            population.sort(key=lambda x: -x.calc_fitness(func))
            population = population[:self.pop_num]

            if population[0].calc_fitness(func) > fittest.calc_fitness(func):
                fittest = population[0]

            avg_fitness = sum_fitnesses / len(fitnesses)
            print(f"Generation #{it}, "
                  f"average gene metrics: {avg_fitness}, "
                  f"fittest gene: {fittest.calc_fitness(func)}")

        return fittest.generate(), fittest.calc_fitness(func)
