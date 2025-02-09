import numpy
import matplotlib.pyplot as plt

times = [[],[],[]]
for row in open("times.csv").readlines():
    for i,p in enumerate(row.split(',')):
        times[i].append( float(p))

x = range(len(times[0]))

plt.plot(x,times[0],label='Python')
plt.plot(x,times[1],label='C++')
plt.plot(x,times[2],label='Go')
plt.legend()
plt.show()
            
