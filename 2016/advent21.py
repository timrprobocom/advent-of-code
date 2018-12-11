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
#word = ['a','b','c','d','e']

word = ['a','b','c','d','e','f','g','h']
word = ['g','c','d','f','b','a','e','h']

def hash(word):
    word = list(word)
    for ln in open('day21.txt'):
#for ln in lines:
        print ln,
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
        print word
    return ''.join(word)

print hash('abcdefgh')
print hash('gcehdbfa')
