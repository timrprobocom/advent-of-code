
nice = sum( 1 for ln in open('day05.txt')
    if not any(( x in ln for x in ('ab','cd','pq','xy')))
    and sum(ln.count(c) for c in 'aeiou') >= 3
    and any( a==b for a,b in zip(ln[:-1],ln[1:]) )
)

print( "Part 1:", nice )


nice = sum( 1 for ln in open('day05.txt') 
    if any(ln[n:n+2] in ln[n+2:] for n in range(len(ln)-2))  
    and any(ln[n] == ln[n+2] for n in range(len(ln)-2))
)

print( "Part 2:", nice )



