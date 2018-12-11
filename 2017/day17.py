#
# Spinlock
#
import sys

buffer = [0]

test = 3
live = 328
p = 0
#for i in range(2018):
for i in range(1,5000000):
    if i % 10000 == 0:
        print "\r%d" % i,
        sys.stdout.flush()
#    print p, i,
    p = (p+live) % i
    buffer.insert(p+1, i)
    p+=1
#    print p, buffer

print buffer[p:p+3]
i = p.index(0)
print buffer[p-2:p+2]
