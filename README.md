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

**Algorithm execution (insertion_sort)**
```
from evo import EvoGen

e = EvoGen(iter_num = 10)
worst_input, worst_time = e.generate_worst_case(insertion_sort, List(20, 25, Int(-20, 20))) 
```