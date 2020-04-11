import operator as op
from functools import reduce
import random
import pickle


def ncr(n, r):  # Code contributed by @dheerosaur
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer / denom


# Func for calculating the total # of ways solving an (x by y) grid
def number_of_paths(x_count, y_count):
    return ncr(x_count + y_count - 2, x_count - 1)


# A function that calculates a random path. 1 is up, 0 is right.
# Can't just use this function as the distribution is not uniform.
def generate_path(x_grid, y_grid, binary=True):
    x_count, y_count = x_grid-1, y_grid-1
    possible = [(0, -1), (1, 0)] if binary else ['up','right']
    choices = []

    while (x_count + y_count) > 0:
        if x_count > 0 and y_count > 0:
            c = possible[random.randint(0, 1)]
            if c == possible[0]:
                y_count -= 1
            else:
                x_count -= 1
            choices.append(c)

        elif y_count == 0:
            choices.append(possible[1])
            x_count -= 1

        else:
            choices.append(possible[0])
            y_count -= 1
    return choices


# A demo that shows a non-uniform distribution for normal generation.
def demo(x_grid, y_grid):
    # print(generate_path(x_grid,y_grid))
    n = 100000
    print(f'Sample Size: {n}')
    ttl_seq = []
    for i in range(n):
        ttl_seq.append(tuple(generate_path(x_grid, y_grid)))

    for i in set(ttl_seq):
        print(f"{i}: {round(ttl_seq.count(i)*100/len(ttl_seq),2)}%")


def demo2(x_grid, y_grid):
    # print(generate_path(x_grid,y_grid))
    n = 10000
    print(f'Sample Size: {n}')
    ttl_seq = []
    for i in range(n):
        ttl_seq.append(tuple(get_random_path(4, 4)))

    for i in set(ttl_seq):
        print(f"{i}: {round(ttl_seq.count(i)*100/len(ttl_seq),2)}%")

# Returns a random path
def get_random_path(x_grid, y_grid, binary = True):
    write = False
    all_paths = None

    with open('data\\all_paths.pkl', 'rb') as file:
        all_paths = pickle.load(file)

    if all_paths.get((x_grid, y_grid)) == None:
        ttl_calc = set()
        while len(ttl_calc) < number_of_paths(x_grid, y_grid):
            ttl_calc.add(tuple(generate_path(x_grid, y_grid, binary)))
        all_paths[(x_grid, y_grid)] = tuple(ttl_calc)
        write = True

    if write:
        with open('all_paths.pkl', 'wb') as file:
            pickle.dump(all_paths, file)

    return random.choice(all_paths[(x_grid, y_grid)])

# def get_all_paths(x_grid, y_grid):
#     all_paths = None
#     with open('all_paths.pkl', 'rb') as file:
#         all_paths = pickle.load(file)
#     return all_paths[(x_grid, y_grid)]

# def get_all_paths_safe(x_grid, y_grid):
#     all_paths = None
#     res = None

#     with open('all_paths.pkl', 'rb') as file:
#         all_paths = pickle.load(file)

#     if all_paths.get((x_grid, y_grid)) == None:
#         ttl_calc = set()
#         while len(ttl_calc) < number_of_paths(x_grid, y_grid):
#             ttl_calc.add(tuple(generate_path(x_grid, y_grid)))
#         all_paths[(x_grid, y_grid)] = tuple(ttl_calc)
#         res = tuple(ttl_calc)

#         with open('all_paths.pkl', 'wb') as file:
#             pickle.dump(all_paths, file)
#             all_paths = None
#     else:
#         res = all_paths[(x_grid, y_grid)]

#     return res

# Initialize and reset dictionary

# Reads the current dictionary form file 
def initialize_dict():
    with open('all_paths.pkl', 'wb') as file:
        pickle.dump({(2, 2): (('up', 'right'), ('right', 'up'))}, file)


# Get all contents of the dictionary
def print_paths_keys():
    with open('all_paths.pkl', 'rb') as file:
        d = pickle.load(file)
        print(f'All Saved Paths Dictionary:\n{d.keys()}')

# print_paths_keys()
# print(get_random_path(4,4))
# demo2(4,4)
# demo(4,4)

# print(generate_path(4,4,False))
