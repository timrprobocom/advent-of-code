# Part 1 is more easily solved in an editor.

real = open('day01.txt').read()
print( "Part 1:", real.count('(')-real.count(')'))

floor = 0
for i,c in enumerate(real):
    if c=='(':
        floor += 1
    if c==')':
        floor -= 1
        if floor < 0:
            print( "Part 2:", i+1 )
            break
