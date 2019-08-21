# gengen
Automatic generation of tests for performance testing using genetic algorithm.

## Developer guide

**NOTE**: the version of python for development is 3.6+

If you want to test or/and show others the usage of your code, then you are more welcome to write unittests.
For reference you can see generic_test.py. We use unittest module and to execute tests you can just run:

**Test execution(example)**
```
python -m unittest -v generic_test.py
```

**Example of execution (insertion_sort)**
```
from generic import List, Int
from evo import EvoGen

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

e = EvoGen(iter_num = 10)
worst_input, worst_time = e.generate_worst_case(insertion_sort, List(20, 25, Int(-20, 20)))
```

## Paper

**GenGen – Input Generation with Genetic Algorithm for Performance Testing**
[1] A. Talipov, S. Torekhan, A. Smagulov, A. Kenzhaliev,  [Input Generation with Genetic Algorithm for Performance Testing](GenGenPaper.pdf)