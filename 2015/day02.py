
sumx = 0
perim = 0
for ln in open('day02.txt'):
    a,b,c = (int(k) for k in ln.rstrip().split('x'))
    sides = a*b, b*c, c*a
    sumx += 2 * sum(sides) + min(sides)
    perim += 2 * (sum((a,b,c)) - max(a,b,c)) + a*b*c

print( "Part 1:", sumx )
print( "Part 2:", perim )


