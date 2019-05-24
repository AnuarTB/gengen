import abc


"""
Base class for all classes of generic types with
abstract mutation, crossover, and generate methods.
"""
class BaseData(abc.ABC):
    """
    The method 'crossover' for a generic class T takes another instance of T
    as an argument and returns *new instance of T*
    NOTE: the instance (self) and the argument (other) are NOT modified
    """
    @abc.abstractmethod
    def crossover(self, other):
        raise NotImplementedError()

    """
    The method 'mutation' for a generic class T returns *new instance of T*
    which was mutated by some pre-defined rules.
    NOTE: original instance is NOT modified.
    """
    @abc.abstractmethod
    def mutation(self):
        raise NotImplementedError()

    """
    The method 'generate' returns the value of the generic class T. So for example
    if T is of class 'generic.Int' then some integer value is returned. Usually the
    generate method has the following structure

        if not self._value:
            ... generate the value with the given constraints ...
        return self._value

    """
    @abc.abstractmethod
    def generate(self):
        raise NotImplementedError()


"""
Base class for classes under test with
implemented mutation, crossover, and generate methods.
"""
class BaseInput(abc.ABC):
    def crossover(self, other):
        """
        Returns the new instance of the class, where
        new instance have crossovered fields.
        """
        instance = self.__class__()
        for k, v in self.__dict__.items():
            if issubclass(v, BaseInput) or issubclass(v, BaseData):
                setattr(instance, k, v.crossover(getattr(other, k)))
        return instance

    def mutation(self):
        """
        Returns the new modified instance of the class whose
        fields were mutated.
        """
        instance = self.__class__()
        for k, v in self.__dict__.items():
            if issubclass(v, BaseInput) or issubclass(v, BaseData):
                setattr(instance, k, v.mutation())
        return instance

    def generate(self):
        """
        Returns the instance with generated value fields.
        """
        instance = self.__class__()
        for k, v in self.__dict__.items():
            if issubclass(v, BaseInput) or issubclass(v, BaseData):
                setattr(instance, k, v.generate())
        return instance
