import numpy
import matplotlib.pyplot as plt

def read(fn):
    t1 = []
    for line in open(fn):
        if 'real' in line:
            _,t = line.strip().split()
            m = t.find('m')
            s = t.find('s')
            mm = int(t[:m])*60
            t1.append( float(t[m+1:s])+mm)

    return t1

py = read('x1')
cpp = read('x2')
x = range(len(py))

plt.plot(x,py,label='Python')
plt.plot(x,cpp,label='C++')
plt.legend()
plt.show()
            
