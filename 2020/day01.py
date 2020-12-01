test = [
1721,
979,
366,
299,
675,
1456
]

data = [int(i) for i in open('day01.txt').readlines()]

for i in range(len(data)):
    for j in range(i+1,len(data)):
        if data[i]+data[j] == 2020:
            print( data[i]*data[j] )

for i in range(len(data)):
    for j in range(i+1,len(data)):
        for k in range(j+1,len(data)):
            if data[i]+data[j]+data[k] == 2020:
                print( data[i]*data[j]*data[k] )
