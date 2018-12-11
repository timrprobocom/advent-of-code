

ips = []
for ln in open('day20.txt'):
    ip = [int(k) for k in ln.strip().split('-')]
    ips.append(ip)

ips.sort()
print len(ips)

i = 0
while i+1 < len(ips):
    print i, len(ips)
    print ips[i]
    while i+1 < len(ips) and ips[i+1][0] <= ips[i+0][1]+1:
        if ips[i+1][1] > ips[i+0][1]:
            ips[i+0][1] = ips[i+1][1]
        ips.pop(i+1)
    i += 1

print len(ips)
print ips[0:9]
print ips[0][1]+1

cnt = 0
for i in range(len(ips)-1):
    cnt += ips[i+1][0] - ips[i][1] - 1

print cnt

