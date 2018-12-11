test = "s1,x3/4,pe/b"
live = open('day16.txt').read().rstrip()

data = live.split(',')


dance = 'abcdefghijklmnop'
#dance = 'abcde'

def round(dance):
    dance = list(dance)
    for move in data:
        if move[0] == 's':
            count = int(move[1:])
            left = dance[:-count]
            right = dance[-count:]
            dance = right + left
        elif move[0] == 'x':
            l,r = (int(k) for k in move[1:].split('/'))
            dance[l],dance[r] = dance[r],dance[l]
        elif move[0] == 'p':
            l,r = move[1:].split('/')
            l = dance.index(l)
            r = dance.index(r)
            dance[l],dance[r] = dance[r],dance[l]
    return ''.join(dance)


track = [dance]

while 1:
    dance = round(dance)
    print dance
    if dance in track:
        print "Repeat in ", len(track)
        break
    track.append(dance)

print track[1000000000%len(track)]

