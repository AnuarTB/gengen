"""
Not a unittest for now
"""
from evo import EvoGen
from generic import Float, Int, List
import logging


def write_log(elapsed_time, input):
    LOG_FORMAT = "%(asctime)s - %(message)s"
    logging.basicConfig(filename = "gengen_logs.log", 
                        level = logging.DEBUG,
                        format = LOG_FORMAT)
    logger = logging.getLogger()
    logger.info((elapsed_time, input))


def f(a):
    """
    Function that accepts float number
    """
    return a + 2


def insertion_sort(tmp):
    arr = tmp[:]
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def bubble_sort(tmp):
    aux = tmp[:]
    while True:
        relaxed = False
        for i in range(len(aux) - 1):
            if aux[i] > aux[i + 1]:
                t = aux[i]
                aux[i] = aux[i + 1]
                aux[i + 1] = t
                relaxed = True
        if not relaxed:
            break
    return aux


def quick_sort(tmp):
    less = []
    equal = []
    greater = []

    if len(tmp) > 1:
        pivot = tmp[0]
        for x in tmp:
            if x < pivot:
                less.append(x)
            elif x == pivot:
                equal.append(x)
            elif x > pivot:
                greater.append(x)
        return quick_sort(less) + equal + quick_sort(greater)
    else:
        return tmp


def main():
    e = EvoGen(5, 10)

    worst, t = e.generate_worst_case(insertion_sort,
                                     List(1000, 2000, Int(-400, 400)))
    print(worst, t)

    worst, t = e.generate_worst_case(bubble_sort,
                                     List(1000, 2000, Int(-400, 400)))

    print(worst, t)

    worst, t = e.generate_worst_case(quick_sort,
                                     List(100000, 200000, Int(-400, 400)))

    print(worst, t)


if __name__ == "__main__":
    main()
