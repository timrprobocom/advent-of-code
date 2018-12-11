
counts = {
    True: 0,
    False: 0
}

tries = []
for ln in open('../Downloads/day3.txt'):
    parts = list(int(k) for k in ln.strip().split())
    tries.extend( parts )
    if len(tries) == 9:
        for i in range(3):
            parts = [tries[i+0],tries[i+3],tries[i+6]]
            maxpart = max(parts)
            rest = sum(parts)-maxpart
            valid = rest > maxpart
            print valid, parts, maxpart, rest
            counts[valid] += 1
        tries=[]

print counts

