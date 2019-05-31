import copy
import random
import time


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

    def mutation(self):
        tmp_args = []
        tmp_kwargs = {}

        for i in range(len(self.input_args)):
            tmp_args.append(self.input_args[i].mutation())

        for k in self.input_kwargs.keys():
            tmp_kwargs[k] = self.input_kwargs[k].mutation()

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
    def __init__(self, pop_num=100, iter_num=300, mut_prob=0.2):
        """
        In order to generate the worst input for the function, this
        wrapper class is instantiated with some of the hyperparameters
        listed below.
        """
        self.pop_num = pop_num  # The population number
        self.iter_num = iter_num  # The number of generations
        self.mut_prob = mut_prob # The probability that the input will mutate
        self.input_class = None

    def create_input(self):
        return copy.deepcopy(self.input_class)

    def select(self, population):
        # TODO(@azretkenzhaliev) Write this function properly
        return population[random.randint(0, 10)]

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
            for _ in range(self.pop_num):
                a = self.select(population)
                b = self.select(population)
                c = a.crossover(b)

                if random.random() < self.mut_prob:
                    c = c.mutation()

                new_population.append(c)

            population += new_population
            population.sort(key=lambda x: -x.calc_fitness(func))
            population = population[:self.pop_num]
            if population[0].calc_fitness(func) > fittest.calc_fitness(func):
                fittest = population[0]

            avg_fitness = sum(map(lambda x: x.calc_fitness(func), population)) / len(population)
            print(f"Generation #{it}, average gene metrics: "
                  f"{avg_fitness}")

        return fittest.generate(), fittest.calc_fitness(func)
