import random

def geom_distr(n, num_buckets=8):
    """
    Randomly selects the number in the range of [0, n)
    """
    cur = 0.5
    r = random.random()
    block_sz = n // num_buckets
    ind = 0
    for i in range(num_buckets - 1):
        if r < cur:
            return block_sz * i + random.randrange(block_sz)
        r -= cur
        cur /= 2.0
    return block_sz * (num_buckets - 1) + random.randrange(block_sz)