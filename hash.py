from evo import EvoGen
from generic import Int, List


class HashMap(object):
    def __init__(self, num_bins=100):
        self.num_bins = num_bins
        self.bins = [[] for i in range(num_bins)]

    def func(self, idx):
        return (idx % self.num_bins + self.num_bins) % self.num_bins

    def add_keys(self, arr):
        for i, e in enumerate(arr):
            idx = self.func(e)
            self.bins[idx].append((e, i))

        for i, e in enumerate(arr):
            idx = self.func(e)
            for t in self.bins[idx]:
                x, j = t[0], t[1]
                if e == x and i == j:
                    break


def main(arr):
    h = HashMap()
    h.add_keys(arr)


if __name__ == "__main__":
    main()
