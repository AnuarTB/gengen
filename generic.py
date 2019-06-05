"""
Implementation of wrappers for generic types.
"""
import copy
import random

from base import BaseData


# TODO(@Azamat7): Implement Int methods
class Int(BaseData):
    def __init__(self, low, high, _value=None):
        self.low = low
        self.high = high
        self._value = _value

    def crossover(self, other):
        bit_self = bin(self.generate())[2:]
        bit_other = bin(other.generate())[2:]

        # new length for the offspring
        child_len = (len(bit_self) + len(bit_other)) // 2

        child, i, j = "", 0, 0
        for _ in range(child_len):
            prob = random.random()

            si = min(len(bit_self) - 1, int(i + 0.5))
            oi = min(len(bit_other) - 1, int(j + 0.5))

            bit = bit_self[si] if prob < 0.5 else bit_other[oi]
            child += bit

            i += len(bit_self) / child_len  # increment self bits
            j += len(bit_other) / child_len  # increment other bits

        child = int("0b" + child, 2)
        if child <= self.low or child >= self.high:
            child = (self.low + self.high) // 2

        return self.__class__(self.low, self.high, child)

    def mutation(self, mutator_id):
        if mutator_id == 0:
            bit_value = bin(self.generate())[2:]
            mutated = ""
            for i in range(len(bit_value)):
                prob = random.random()
                bit = str(random.randint(0, 1)) if prob > 0.9 else bit_value[i]
                mutated += bit
            return self.__class__(self.low, self.high, int("0b" + mutated, 2))
        return self

    def generate(self):
        if not self._value:
            self._value = random.randint(self.low, self.high)
        return self._value


# TODO(@Azamat7): Implement Float methods (see Int for reference)
class Float(BaseData):
    def __init__(self, low, high, _value=None):
        self.low = low
        self.high = high
        self._value = _value

    def crossover(self, other):
        return self.__class__(self.low, self.high,
                              (self.generate() + other.generate()) / 2)

    def mutation(self, mutator_id=0):
        if mutator_id == 0:
            bit_value = str(self.generate())
            dot = [p for p, c in enumerate(bit_value) if c == "."][0]
            mutated = bit_value[:dot + 1]
            for i in range(dot + 1, len(bit_value)):
                prob = random.random()
                bit = str(random.randint(0, 9)) if prob > 0.9 else bit_value[i]
                mutated += bit
            return self.__class__(self.low, self.high, float(mutated))
        return mutator_id

    def generate(self):
        if not self._value:
            self._value = random.uniform(self.low, self.high)
        return self._value


# TODO(@Azamat7): Implement String methods (see Int for reference)
class String(BaseData):
    def __init__(self, low, high, chars, _value=None):
        self.low = low  # should be at least 1
        self.high = high
        self.chars = chars
        self._value = _value

    def crossover(self, other):
        parent1 = self.generate()
        parent2 = other.generate()

        # new length for the offspring
        child_len = (len(parent1) + len(parent2)) // 2
        child, i, j = "", 0, 0

        for _ in range(child_len):
            prob = random.random()

            si = min(len(parent1) - 1, int(i + 0.5))
            oi = min(len(parent2) - 1, int(j + 0.5))

            bit = parent1[si] if prob < 0.5 else parent2[oi]
            child += bit

            i += len(parent1) / child_len    # increment self bits
            j += len(parent2) / child_len   # increment other bits

        return self.__class__(self.low, self.high, self.chars, child)

    def mutation(self, mutator_id=0):
        if mutator_id == 0:
            original = self.generate()
            mutated = ""
            for i in range(len(original)):
                prob = random.random()
                if prob > 0.9:
                    char = str(self.chars[random.randint(0, len(self.chars) - 1)])
                else:
                    char = original[i]

                mutated += char
            return self.__class__(self.low, self.high, self.chars, mutated)
        return self

    def generate(self):
        if not self._value:
            length = random.randint(self.low, self.high)
            value = ""
            for _ in range(length):
                index = random.randint(0, len(self.chars) - 1)
                value += self.chars[index]
            self._value = value
        return self._value


# TODO(@shynar88): Implement List methods (see Int for reference)
class List(BaseData):
    def __init__(self, low, high, elem, _value=None):
        self.low = low
        self.high = high
        self.elem = elem
        self._value = _value

    def crossover(self, other):
        shortest_len = min(len(self.generate()), len(other.generate()))
        crossover_point = random.randint(0, shortest_len - 1)
        rand_int = random.randint(0, 1)
        if rand_int == 1:
            child = (self._value[:crossover_point] +
                     other._value[crossover_point:])
        else:
            child = (self._value[crossover_point:] +
                     other._value[:crossover_point])
        return self.__class__(self.low, self.high, self.elem, child)

    def mutation(self, mutator_id=0):
        original = self.generate()
        mutated = original[:]

        if mutator_id == 0:
            for i in range(len(mutated)):
                prob = random.random()
                elem = self.elem.generate() if prob > 0.9 else mutated[i]
                elem = copy.deepcopy(self.elem).generate() if prob > 0.9 else mutated[i]
                mutated[i] = elem
            return self.__class__(self.low, self.high, self.elem, mutated)

        elif mutator_id == 1:
            fraction = max(int(len(mutated) * 0.05), 1)
            for i in range(fraction):
                left_index = max(0, random.randint(0, len(mutated) - 2))
                right_index = max(0, random.randint(0, len(mutated) - 1))
                if left_index == right_index:
                    right_index += 1
                t = mutated[left_index]
                mutated[left_index] = mutated[right_index]
                mutated[right_index] = t
            return self.__class__(self.low, self.high, self.elem, mutated)

        else:
            return self

    def generate(self):
        if not self._value:
            length = random.randint(self.low, self.high)
            value = []
            for _ in range(length):
                elem = copy.deepcopy(self.elem).generate()
                value.append(elem)
            self._value = value
        return self._value


# TODO(@shynar88): Implement Tuple methods (see Int for reference)
class Tuple(BaseData):
    def __init__(self, low, high, elem, _value=None):
        self.low = low
        self.high = high
        self.elem = elem
        self._value = _value

    def crossover(self, other):
        self_list = List(self.low, self.high, self.elem, list(self._value))
        other_list = List(other.low, other.high. other.elem, list(other._value))
        child = tuple(self_list.crossover(other_list)._value)
        return self.__class__(self.low, self.high, self.elem, child)

    def mutation(self, mutator_id=0):
        if mutator_id == 0:
            self_list = List(self.low, self.high, self.elem, list(self._value))
            mutated = tuple(self_list.mutation()._value)
            return self.__class__(self.low, self.high, self.elem, mutated)
        return self

    def generate(self):
        if not self._value:
            self_list = List(self.low, self.high, self.elem, list(self._value))
            self._value = tuple(self_list.generate())
        return self._value


class Dict(BaseData):
    """
    User provides what keys can be in the dictionary and their types.
    """
    def __init__(self, key_dict=None):
        self._value = None
        self.key_dict = key_dict if key_dict else {}

    def crossover(self, other):
        new_dict = self.__class__()
        for k in self.key_dict.keys():
            new_dict.key_dict[k] = self._value[k].crossover(other._value[k])
        return new_dict

    def mutation(self, mutator_id=0):
        if mutator_id == 0:
            new_dict = copy.deepcopy(self)
            for k in self._value.keys():
                new_dict.key_dict[k] = new_dict.key_dict[k].mutation()
            return new_dict
        return self

    def generate(self):
        if not self._value:
            self._value = dict()
            for k in self.key_dict.keys():
                self._value[k] = self.key_dict[k].generate()
        return self._value
