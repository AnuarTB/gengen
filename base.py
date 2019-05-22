import abc


"""
Base class for all classes of generic types with
abstract mutation, crossover, and generate methods.
"""
class BaseData(abc.ABC):
    @abc.abstractmethod
    def crossover(self, other):
        raise NotImplementedError()

    @abc.abstractmethod
    def mutation(self):
        raise NotImplementedError()

    @abs.abstractmethod
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
