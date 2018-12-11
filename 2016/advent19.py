
test = 5
chk = 100
prod = 3018458


def onepass( table, start ):
    nxt = start ^ (len(table) & 1)
    newtable = []
    if start:
        for i in range(len(table)):
            if i & 1:
                newtable.append(table[i])
    else:
        for i in range(len(table)):
            if not i & 1:
                newtable.append(table[i])
    return newtable, nxt
    
table = range(1,prod+1)
nxt = 0
while len(table) > 1:
    table, nxt = onepass( table, nxt )
    print table, nxt
