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
        bitSelf = bin(self._value)[2:]
        bitOther = bin(other._value)[2:]

        childLen = (len(bitSelf) + len(bitOther)) // 2   # new length for the offspring
        child, i, j = "", 0, 0

        for _ in range(childLen):
            prob = random.random() 
            bit = bitSelf[int(i+0.5)] if prob<0.5 else bitOther[int(j+0.5)]
            child += bit
            i += len(bitSelf)/ childLen    # increment self bits
            j += len(bitOther)/ childLen   # increment other bits

        return int("0b"+child,2)

    def mutation(self):
        bitValue = bin(value)[2:]
        mutated = ""
        for i in range(len(bitValue)):
            prob = random.random() 
            bit = str(random.randint(0,1)) if prob>0.9 else bitValue[i]
            mutated += bit
        self._value = int("0b"+mutated,2) 

    def generate(self):
        if not self._value:
            self._value = random.randint(self.low, self.high)
        return self._value


#TODO(@Azamat7): Implement Float methods (see Int for reference)
class Float(BaseData):
    def __init__(self, low, high):
        self.low = low
        self.high = high
        self._value = None

    def crossover(self, other):
        return (self._value+other._value)/2

    def mutation(self):
        bitValue = str(self._value)
        dot = [p for p,c in enumerate(bitValue) if c=="."][0]
        mutated = bitValue[:dot+1]
        for i in range(dot+1,len(bitValue)):
            prob = random.random() 
            bit = str(random.randint(0,9)) if prob>0.9 else bitValue[i]
            mutated += bit
        self._value = float(mutated) 

    def generate(self):
        if not self._value:
            self._value = random.uniform(self.low, self.high)
        return self._value


#TODO(@Azamat7): Implement String methods (see Int for reference)
class String(BaseData):
    def __init__(self, low, high, chars):
        self.low = low
        self.high = high
        self._value = None
        self.chars = chars

    def crossover(self, other):
        parent1 = self._value
        parent2 = other._value

        childLen = (len(parent1) + len(parent2)) // 2   # new length for the offspring
        child, i, j = "", 0, 0

        for _ in range(childLen):
            prob = random.random() 
            bit = parent1[int(i+0.5)] if prob<0.5 else parent2[int(j+0.5)]
            child += bit
            i += len(parent1)/ childLen    # increment self bits
            j += len(parent2)/ childLen   # increment other bits

        return child

    def mutation(self):
        original = self._value
        mutated = ""
        for i in range(len(original)):
            prob = random.random() 
            char = str(self.chars[random.randint(0,len(self.chars))]) if prob>0.9 else original[i]
            mutated += char
        self._value = mutated 

    def generate(self):
        if not self._value:
            length = random.randint(low,high)
            value = ""
            for _ in range(length):
                index = random.randint(0,len(self.chars))
                value += self.chars[index]
            self._value = value
        return self._value


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
