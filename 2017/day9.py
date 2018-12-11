tests = """\
{}
{{{}}}
{{},{}}
{{{},{},{{}}}}
{<a>,<a>,<a>,<a>}
{{<ab>},{<ab>},{<ab>},{<ab>}}
{{<!!>},{<!!>},{<!!>},{<!!>}}
{{<a!>},{<a!>},{<a!>},{<ab>}}""".splitlines()

live = open('day9.txt').readlines()

data = live

# state 0

def parse(ln,nest=0):
#    print ''.join(ln)
    sumnest = nest
    escape = 0
    state = 0
    while ln:
        c = ln.pop(0)
        if escape:
            escape = 0
        elif c == '!':
            escape = 1
        elif state == 'g':
            if c == '>':
                state = 0
        elif c == '<':
            state = 'g'
        elif c == '{':
            sumnest += parse(ln, nest+1)
        elif c == '}':
            break
#    print nest, sumnest
    return sumnest



for ln in data:
    m = parse(list(ln))
    print m, ln
