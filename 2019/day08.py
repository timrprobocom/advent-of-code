
def part1():
    min0 = 99999
    for ln in open('day08a.txt'):
        i0 = len(list(1 for k in ln if k == '0'))
        i1 = len(list(1 for k in ln if k == '1'))
        i2 = len(list(1 for k in ln if k == '2'))
        ccc = ''
        if i0 < min0:
            ccc = '***'
            best = i1*i2
            min0 = i0

        print( i0, i1, i2, i1*i2, ccc )

    print( "Part 1:", best )

def part2():
    s = ['2']*(25*6)
    for ln in open('day08a.txt'):
        for i,c in enumerate(ln.strip()):
            if s[i] == '2':
                s[i] = c
    print( "Part 2:" )
    for i in range(0,150,25):
        print( ''.join(s[i:i+25]).replace('0',' ') )

part1()
part2()

