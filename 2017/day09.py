import sys
TEST = 'test' in sys.argv
DEBUG = 'debug' in sys.argv

tests = """\
<>
<random characters>
<<<<>
<{!>}>
<!!>
<!!!>>
<{o"i!a,<{i<a>
{}
{{{}}}
{{},{}}
{{{},{},{{}}}}
{<a>,<a>,<a>,<a>}
{{<ab>},{<ab>},{<ab>},{<ab>}}
{{<!!>},{<!!>},{<!!>},{<!!>}}
{{<a!>},{<a!>},{<a!>},{<ab>}}""".splitlines()

live = open('day9.txt').read().splitlines()

data = tests if TEST else live

# state 0

def parse(ln,nest=0):
    global garbage
    sumnest = nest
    escape = 0
    state = 0
    while ln:
        c = ln.pop(0)
        if state == 'g' and c != '>' and not escape:
            garbage += 1
        if escape:
            escape = 0
        elif c == '!':
            garbage -= 1
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
    return sumnest



for ln in data:
    garbage = 0
    m = parse(list(ln))
    if DEBUG:
        print(m)
    print('Part 1:', m)
    print('Part 2:', garbage)
