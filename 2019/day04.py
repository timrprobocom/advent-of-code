ranges = (254032,789860+1)

def valid(pw,part):
    dig = list(int(k) for k in str(pw))
    cnts = [0]*10
    for c in range(6):
        if c < 5 and dig[c] > dig[c+1]:
            return False
        cnts[dig[c]] += 1

# part 1
#    print( cnts )
    if part == 1:
        return any(k >= 2 for k in cnts )
# part 2
    else:
        return 2 in cnts

tests = ( 111111, 223450, 123789, 112233, 123444, 111122 )

for part in (1,2):
    print( "Part ", part )
    for t in tests:
        print( t,  valid( t, part ) )
     
    cnt = 0
    for r in range( *ranges ):
        if valid(r, part):
            cnt += 1
        
    print( cnt )
