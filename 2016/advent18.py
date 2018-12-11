#
# A vEriation of the Game of Life.
#
# 1,1,0 => 1
# 0,1,1 => 1
# 1,0,0 => 1
# 0,0,1 => 1

lookup = [ 0, 1, 0, 1, 1, 0, 1, 0 ]


def nextRow( row ):
    newrow = []
    fake = [0] + row + [0]
    for i in range(len(row)):
        nbr = fake[i]*4+fake[i+1]*2+fake[i+2]
        newrow.append( lookup[nbr] )
    return newrow

ipt = ".^..^....^....^^.^^.^.^^.^.....^.^..^...^^^^^^.^^^^.^.^^^^^^^.^^^^^..^.^^^.^^..^.^^.^....^.^...^^.^."

#baserow = [0, 0, 1, 1, 0]
#baserow = [0,1,1,0,1,0,1,1,1,1]
baserow = [1 if c=='^' else 0 for c in ipt]
row = baserow
sumx = len(row) - sum(row)
print row
for i in range(399999):
    row = nextRow(row)
    sumx += len(row) - sum(row)

print sumx
