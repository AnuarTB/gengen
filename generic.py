"""
Implementation of wrappers for generic types.
"""
import random

from base import BaseData


#TODO(@Azamat7): Implement Int methods
class Int(BaseData):
    def __init__(self, low, high):
        self.low = low
        self.high = high
        self._value = None

    def crossover(self, other):
        raise NotImplementedError()

    def mutation(self):
        raise NotImplementedError()

    def generate(self):
        if not self._value:
            self._value = random.randint(self.low, self.high)
        return self._value


#TODO(@Azamat7): Implement Float methods (see Int for reference)
class Float(BaseData):
    def crossover(self, other):
        raise NotImplementedError()

    def mutation(self):
        raise NotImplementedError()

    def generate(self):
        raise NotImplementedError()


#TODO(@Azamat7): Implement String methods (see Int for reference)
class String(BaseData):
    def crossover(self, other):
        raise NotImplementedError()

    def mutation(self):
        raise NotImplementedError()

    def generate(self):
        raise NotImplementedError()


#TODO(@shynar88): Implement List methods (see Int for reference)
class List(BaseData):
    def crossover(self, other):
        raise NotImplementedError()

    def mutation(self):
        raise NotImplementedError()

    def generate(self):
        raise NotImplementedError()


#TODO(@shynar88): Implement Tuple methods (see Int for reference)
class Tuple(BaseData):
    def crossover(self, other):
        raise NotImplementedError()

    def mutation(self):
        raise NotImplementedError()

    def generate(self):
        raise NotImplementedError()


#TODO(@azretkenzhaliev, @anuartb): Implement Dict methods (see Int for reference)
class Dict(BaseData):
    def crossover(self, other):
        raise NotImplementedError()

    def mutation(self):
        raise NotImplementedError()

    def generate(self):
        raise NotImplementedError()
