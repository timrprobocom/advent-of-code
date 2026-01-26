import sys
TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

# another interpreter.

lines = [
"swap position 4 with position 0",
"swap letter d with letter b",
"reverse positions 0 through 4",
"rotate left 1",
"move position 1 to position 4",
"move position 3 to position 0",
"rotate based on position of letter b",
"rotate based on position of letter d"
]

if TEST:
    data = lines.splitlines()
else:
    data = open('day21.txt').read().splitlines()

#word = ['a','b','c','d','e','f','g','h']
#word = ['g','c','d','f','b','a','e','h']

def hash(data, word):
    word = list(word)
    for ln in data:
        if DEBUG:
            print( ln, end=' ' )
        parts = ln.strip().split()
        if parts[0] == 'move':
            src = int(parts[2])
            dst = int(parts[5])
            x = word.pop(src)
            word.insert( dst, x )
        elif parts[0] == 'swap':
            if parts[1] == 'position':
                src = int(parts[2])
                dst = int(parts[5])
                srcx = word[src]
                dstx = word[dst]
            else:
                srcx = parts[2]
                dstx = parts[5]
                src = word.index(srcx)
                dst = word.index(dstx)
            word[src] = dstx
            word[dst] = srcx
        elif parts[0] == 'reverse':
            start = int(parts[2])
            end = int(parts[4])
            sub = word[start:end+1]
            sub.reverse()
            word = word[:start] + sub + word[end+1:]
        elif parts[0] == 'rotate':
            if parts[1] == 'based':
                qty = word.index(parts[6]) + 1
                if qty > 4:
                    qty = (qty % len(word)) + 1
            else:
                qty = int(parts[2])
            if parts[1] == 'left':
                word = word[qty:] + word[:qty]
            else:
                word = word[-qty:] + word[:-qty]
        if DEBUG:
            print( word )
    return ''.join(word)

unmap = [ 1, 1, -2, 2, -1, 3, 0, 4]

def part2(data, word):
    data.reverse()
    word = list(word)
    if DEBUG:
        print( word )
    for ln in data:
        if DEBUG:
            print( ln )
        parts = ln.strip().split()
        if parts[0] == 'move':
    # Move you just reverse the numbers.
            dst = int(parts[2])
            src = int(parts[5])
            x = word.pop(src)
            word.insert( dst, x )
        elif parts[0] == 'swap':
    # Swap is the same.
            if parts[1] == 'position':
                src = int(parts[2])
                dst = int(parts[5])
                srcx = word[src]
                dstx = word[dst]
            else:
                srcx = parts[2]
                dstx = parts[5]
                src = word.index(srcx)
                dst = word.index(dstx)
            word[src] = dstx
            word[dst] = srcx
        elif parts[0] == 'reverse':
    # Reverse is the same.
            start = int(parts[2])
            end = int(parts[4])
            sub = word[start:end+1]
            sub.reverse()
            word = word[:start] + sub + word[end+1:]
        elif parts[0] == 'rotate':
    # Rotate unbased is easy, just swap em.
    # Rotate based???
            if parts[1] == 'based':
                qty = word.index(parts[6])
                qty = unmap[qty]
                word = word[qty:] + word[:qty]
            else:
                qty = int(parts[2])
                if parts[1] == 'left':
                    word = word[-qty:] + word[:-qty]
                else:
                    word = word[qty:] + word[:qty]
        if DEBUG:
            print( word )
    return ''.join(word)

print('Part 1:', hash(data, 'abcdefgh'))
if DEBUG:
    print( hash(data, 'gcehdbfa') )
print('Part 2:', part2(data, 'fbgdceah'))
