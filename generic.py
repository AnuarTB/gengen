"""
Implementation of wrappers for generic types.
"""
import random
import copy

from base import BaseData


#TODO(@Azamat7): Implement Int methods
class Int(BaseData):
    def __init__(self, low, high, _value=None):
        self.low = low
        self.high = high
        self._value = _value

    def crossover(self, other):
        bitSelf = bin(self.generate())[2:]
        bitOther = bin(other.generate())[2:]
        childLen = (len(bitSelf) + len(bitOther)) // 2   # new length for the offspring
        child, i, j = "", 0, 0

        for _ in range(childLen):
            prob = random.random()
            si = min(len(bitSelf)-1,int(i+0.5))
            oi = min(len(bitOther)-1,int(j+0.5))
            bit = bitSelf[si] if prob<0.5 else bitOther[oi]
            child += bit
            i += len(bitSelf)/ childLen    # increment self bits
            j += len(bitOther)/ childLen   # increment other bits

        child = int("0b"+child,2)
        if child<=self.low or child>=self.high:
            child = (self.low+self.high)//2

        return self.__class__(self.low, self.high, child)

    def mutation(self):
        bitValue = bin(self.generate())[2:]
        mutated = ""
        for i in range(len(bitValue)):
            prob = random.random()
            bit = str(random.randint(0,1)) if prob>0.9 else bitValue[i]
            mutated += bit
        return self.__class__(self.low, self.high, int("0b"+mutated,2))
        self._value = int("0b"+mutated,2)

    def generate(self):
        if not self._value:
            self._value = random.randint(self.low, self.high)
        return self._value


#TODO(@Azamat7): Implement Float methods (see Int for reference)
class Float(BaseData):
    def __init__(self, low, high, _value=None):
        self.low = low
        self.high = high
        self._value = _value

    def crossover(self, other):
        return self.__class__(
            self.low,
            self.high,
            (self.generate()+other.generate())/2)

    def mutation(self):
        bitValue = str(self.generate())
        dot = [p for p,c in enumerate(bitValue) if c=="."][0]
        mutated = bitValue[:dot+1]
        for i in range(dot+1,len(bitValue)):
            prob = random.random()
            bit = str(random.randint(0,9)) if prob>0.9 else bitValue[i]
            mutated += bit
        return self.__class__(
            self.low,
            self.high,
            float(mutated)
        )

    def generate(self):
        if not self._value:
            self._value = random.uniform(self.low, self.high)
        return self._value


#TODO(@Azamat7): Implement String methods (see Int for reference)
class String(BaseData):
    def __init__(self, low, high, chars, _value=None):
        self.low = low
        self.high = high
        self.chars = chars
        self._value = _value

    def crossover(self, other):
        parent1 = self.generate()
        parent2 = other.generate()

        childLen = (len(parent1) + len(parent2)) // 2   # new length for the offspring
        child, i, j = "", 0, 0

        for _ in range(childLen):
            prob = random.random()
            bit = parent1[int(i+0.5)] if prob<0.5 else parent2[int(j+0.5)]
            child += bit
            i += len(parent1)/ childLen    # increment self bits
            j += len(parent2)/ childLen   # increment other bits

        return self.__class__(self.low, self.high, self.chars, child)

    def mutation(self):
        original = self.generate()
        mutated = ""
        for i in range(len(original)):
            prob = random.random()
            char = str(self.chars[random.randint(0,len(self.chars))]) if prob>0.9 else original[i]
            mutated += char
        return self.__class__(self.low, self.high, self.chars, mutated)

    def generate(self):
        if not self._value:
            length = random.randint(self.low, self.high)
            value = ""
            for _ in range(length):
                index = random.randint(0,len(self.chars))
                value += self.chars[index]
            self._value = value
        return self._value


#TODO(@shynar88): Implement List methods (see Int for reference)
class List(BaseData):
    def __init__(self, low, high, elem, _value=None):
        self.low = low
        self.high = high
        self.elem = elem
        self._value = _value

    def crossover(self, other):
        shortestLen = min(len(self.generate()), len(other.generate()))
        crossoverPoint = random.randint(0, shortestLen-1)
        randInt = random.randint(0, 1)
        child = []
        if randInt == 1:
            child = self._value[:crossoverPoint] + other._value[crossoverPoint:]
        else:
            child = other._value[:crossoverPoint] + self._value[crossoverPoint:]
        return self.__class__(self.low, self.high, self.elem, child)

    def mutation(self):
        original = self.generate()
        mutated = []
        for i in range(len(original)):
            prob = random.random()
            elem = copy.deepcopy(self.elem).generate() if prob>0.9 else original[i]
            mutated.append(elem)
        return self.__class__(self.low, self.high, self.elem, mutated)

    def generate(self):
        if not self._value:
            length = random.randint(self.low, self.high)
            value = []
            for _ in range(length):
                elem = copy.deepcopy(self.elem).generate()
                value.append(elem)
            self._value = value
        return self._value


#TODO(@shynar88): Implement Tuple methods (see Int for reference)
class Tuple(BaseData):
    def __init__(self, low, high, elem, _value=None):
        self.low = low
        self.high = high
        self.elem = elem
        self._value = _value

    def crossover(self, other):
        selfList = List(self.low, self.high, self.elem, list(self._value))
        otherList = List(other.low, other.high. other.elem, list(other._value))
        child = tuple(selfList.crossover(otherList)._value)
        return self.__class__(self.low, self.high, self.elem, child)

    def mutation(self):
        selfList = List(self.low, self.high, self.elem, list(self._value))
        mutated = tuple(selfList.mutation()._value)
        return self.__class__(self.low, self.high, self.elem, mutated)

    def generate(self):
        if not self._value:
            selfList = List(self.low, self.high, self.elem, list(self._value))
            self._value = tuple(selfList.generate())
        return self._value


class Dict(BaseData):
    """
    User provides what keys can be in the dictionary and their types.
    """
    def __init__(self, key_dict=None):
        self._value = None
        self.key_dict = key_dict if key_dict else dict()

    def crossover(self, other):
        new_dict = self.__class__()
        for k in self.key_dict.keys():
            new_dict[k] = self._value[k].crossover(other._value[k])
        return new_dict

    def mutation(self):
        new_dict = copy.deepcopy(self)
        for k in self._value.keys():
            new_dict[k] = new_dict[k].mutation()
        return new_dict

    def generate(self):
        if not self._value:
            self._value = dict()
            for k in key_dict.keys():
                self._value[k] = key_dict[k].generate()
        return self._value
