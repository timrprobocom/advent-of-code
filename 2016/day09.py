import sys

TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

data = (
('ADVENT', 'ADVENT'),
('A(1x5)BC', 'ABBBBBC'),
('(3x3)XYZ', 'XYZXYZXYZ'),
('A(2x2)BCD(2x2)EFG','ABCBCDEFEFG'),
('(6x1)(1x3)A','(1x3)A'),
('X(8x2)(3x3)ABCY','X(3x3)ABC(3x3)ABCY')
)

def decompress1(s):
    chars = 0
    while 1:
        lpar = s.find( '(' )
        if lpar < 0:
            return chars + len(s)
        rpar = s.find( ')' )

        cnt,rep = [int(k) for k in s[lpar+1:rpar].split('x')]
        chars += lpar + cnt * rep
        s = s[rpar+1+cnt:]
    return 0

def decompress2(s):
    if DEBUG:
        print( s )
    chars = 0
    while 1:
        lpar = s.find( '(' )
        if lpar < 0:
            if DEBUG:
                print( chars + len(s) )
            return chars + len(s)
        rpar = s.find( ')' )

        cnt,rep = [int(k) for k in s[lpar+1:rpar].split('x')]
        chars += lpar + decompress2(s[rpar+1:rpar+1+cnt]) * rep
        if DEBUG:
            print( lpar, rpar, cnt, rep, chars, s )
        s = s[rpar+1+cnt:]
    return 0


totlen = [0,0]
#for inx,outx in data:
for inx in open('day9.txt').readlines():
    inx = inx.strip()
    totlen[0] += decompress1(inx)
    totlen[1] += decompress2(inx)

print('Part 1:', totlen[0])
print('Part 2:', totlen[1])
