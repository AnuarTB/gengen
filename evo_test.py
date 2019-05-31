"""
Not a unittest for now
"""
from evo import EvoGen
from generic import Float, Int, List


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
    worst, t = e.generate_worst_case(insertion_sort,
                                     List(100, 150, Int(-400, 400)))
    print("The worst input:")
    print(worst)
    print(f"The runtime of the function for this input is: {t}")


if __name__ == "__main__":
    main()
