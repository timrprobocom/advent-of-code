test = "2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2"
live = open('day08.txt').read()

data = list(int(k) for k in test.split())
data = list(int(k) for k in live.split())

# count of child nodes
# count of metadata
#   child nodes
# metadata

summeta = 0
def read(data):
    global summeta
    nch = data.pop(0)
    nmd = data.pop(0)
    print nch, nmd
    for i in range(nch):
        read(data)
    
    for i in range(nmd):
        meta = data.pop(0)
        summeta += meta


#read(data)
#print summeta


def read2(data):
    nch = data.pop(0)
    nmd = data.pop(0)
    print nch, nmd
    
    nodevals = list(read2(data) for i in range(nch))
    print nch, nmd, 'nodevals', nodevals
    
    metadata = data[:nmd]
    for i in range(nmd):
        data.pop(0)
    print nch, nmd, 'metadata', metadata

    value = 0
    if nch:
        print nch, nmd, 
        for i in metadata:
            print i,
            if i > 0 and i-1 < nch:
                value += nodevals[i-1]
    else:
        value = sum(metadata)

    print " == ", value
    return value

print read2(data)
