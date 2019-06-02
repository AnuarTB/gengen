"""
Not a unittest for now
"""
from evo import EvoGen
from generic import Float, Int, List
from time import process_time
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


def main():
    e = EvoGen()
    run_time = process_time()
    worst, t = e.generate_worst_case(insertion_sort,
                                     List(100, 150, Int(-400, 400)))
    elapsed_time = process_time() - run_time
    write_log(elapsed_time, worst)
    print("The worst input:")
    print(worst)
    print(f"The runtime of the function for this input is: {t}")


if __name__ == "__main__":
    main()
