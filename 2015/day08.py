
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


sun = 0
sesc = 0
for ln in open('day08.txt'):
    ln = ln.strip()
    sun += unescape(ln)
    sesc += escape(ln)

print( "Part 1:", sun )
print( "Part 2:", sesc )
