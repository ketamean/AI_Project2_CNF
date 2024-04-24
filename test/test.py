import itertools
mylist = [2,2,3,4,5]
combinations = list(itertools.combinations(mylist, 3))
for item in combinations:
    t = list(item)

    print(t)