

nice = 0
for ln in open('day05.txt'):
    if any(( ln.find(x)>=0 for x in ('ab','cd','pq','xy'))):
        continue
    if sum(ln.count(c) for c in 'aeiou') < 3:
        continue
    ok = False
    for n in range(len(ln)-1):
        if ln[n] == ln[n+1]:
            ok = True
            nice += 1
            break

print( "Part 1:", nice )

nice = 0
for ln in open('day05.txt'):
    s1, s2 = False, False
    for n in range(len(ln)-2):
        if ln.find( ln[n:n+2], n+2) >= 0:
            s1 = True
        if ln[n] == ln[n+2]:
            s2 = True
    if s1 and s2:
        nice += 1

print( "Part 2:", nice )



