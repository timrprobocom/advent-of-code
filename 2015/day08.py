
def unescape(s):
    sz = 2
    esc = False
    for c in s:
        if esc:
            if c == 'x':
                sz += 3
            else:
                sz += 1
            esc = False
        elif c == '\\':
            esc = True
    return sz

def escape(s):
    sz = 2
    for c in s:
        if c == '"':
            sz += 1
        elif c == '\\':
            sz += 1
    return sz;

sun = sum(unescape(ln.strip()) for ln in open('day08.txt'))
sesc = sum(escape(ln.strip()) for ln in open('day08.txt'))

print( "Part 1:", sun )
print( "Part 2:", sesc )
