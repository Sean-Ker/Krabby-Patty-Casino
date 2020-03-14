import operator as op
from functools import reduce
import random

x_grid = 4
y_grid = 4


def ncr(n, r):  # Code contributed by @dheerosaur
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer / denom


# print(ncr(x_count + y_count - 2, x_count - 1))

print(f"Grid Size: {x_grid}x{y_grid}")
# Generates path. 1 is up, 0 is right.


def generate_path(x_grid, y_grid):

    x_count, y_count = x_grid-1, y_grid-1
    choices = []
    while (x_count + y_count) > 0:
        if x_count > 0 and y_count > 0:
            c = ['up', 'right'][random.randint(0, 1)]
            if c == 'up':
                y_count -= 1
            else:
                x_count -= 1
            choices.append(c)
        elif y_count == 0:
            choices.append('right')
            x_count -= 1
        else:
            choices.append('up')
            y_count -= 1
    return choices


# print(generate_path(x_grid,y_grid))
n = 100000
print(f'Sample Size: {n}')
ttl_seq = []
for i in range(n):
    ttl_seq.append(tuple(generate_path(x_grid, y_grid)))

for i in set(ttl_seq):
    print(f"{i}: {round(ttl_seq.count(i)*100/len(ttl_seq),2)}%")
