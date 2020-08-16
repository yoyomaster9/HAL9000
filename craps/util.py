# will contain useful functions for later on.

def col(x, padding = 2, uniform = False):
    l = [row.copy() for row in x] # copy data instead of assignment
    for i in range(len(l)-1):
        if len(l[i]) != len(l[i+1]):
            raise Exception('Check dimensions before using col')
    colwidths = [max([len(row[i]) for row in l]) + padding for i in range(len(l[0]))]

    if uniform:
        colwidths = [max(colwidths) for x in colwidths]

    for i in range(len(l[0])):
        l[0][i] = l[0][i].center(colwidths[i], ' ')

    for x in range(1, len(l)):
        for y in range(len(l[0])):
            l[x][y] = l[x][y] + ' '*(colwidths[y] - len(l[x][y]))

    l.insert(1, ['='*i for i in colwidths])

    return '\n'.join(['|'.join(row) for row in l])
