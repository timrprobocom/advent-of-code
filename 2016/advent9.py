data = (
('ADVENT', 'ADVENT'),
('A(1x5)BC', 'ABBBBBC'),
('(3x3)XYZ', 'XYZXYZXYZ'),
('A(2x2)BCD(2x2)EFG','ABCBCDEFEFG'),
('(6x1)(1x3)A','(1x3)A'),
('X(8x2)(3x3)ABCY','X(3x3)ABC(3x3)ABCY')
)

def decompress(s):
    if s.find('(') < 0:
        return len(s)

    chars = 0
    print s
    nxt = 0
    while 1:
        lpar = s.find( '(' )
        if lpar < 0:
            print chars + len(s)
            return chars + len(s)
        rpar = s.find( ')' )

        cnt,rep = [int(k) for k in s[lpar+1:rpar].split('x')]
        chars += lpar + decompress(s[rpar+1:rpar+1+cnt]) * rep
        print lpar, rpar, cnt, rep, chars, s
        s = s[rpar+1+cnt:]
    return 0


totlen = 0
#for inx,outx in data:
for inx in open('../Downloads/day9.txt').readlines():
    m = decompress(inx.strip())
    totlen += m
    print m

print totlen
