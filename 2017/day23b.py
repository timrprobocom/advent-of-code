import math

cnt = 0
for i in range(106500,123501,17):
    prime = True
    for j in range(2,int(math.sqrt(i)+2)):
        if i % j == 0:
            prime = False
            cnt += 1
            break
#    if prime:
#        print i, "prime"
#        cnt += 1

print cnt
