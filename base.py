import random
import copy

"""
NOTE: All inputs must be extended from this class

If you want to combine inputs in your own way you
can overwrite the combine method which takes as an argument
the other instance of the same class and returns the new
combined instance.
"""
class BaseInput(object):
    def combine(self, other):
        if random.randint(0, 1):
            return copy.deepcopy(self)
        else:
            return copy.deepcopy(other)