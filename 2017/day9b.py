tests = """\
<>
<random characters>
<<<<>
<{!>}>
<!!>
<!!!>>
<{o"i!a,<{i<a>""".splitlines()

live = open('day9.txt').readlines()

data = live

# state 0

def parse(ln):
    count = 0
    escape = 0
    garbage = 0
    while ln:
        c = ln.pop(0)
        if escape:
            escape = 0
        elif c == '!':
            escape = 1
        elif garbage:
            if c == '>':
                garbage = 0
            else:
                count += 1
        elif c == '<':
            garbage = 1
        elif c == '{':
            count += parse(ln)
        elif c == '}':
            break
    return count



for ln in data:
    print parse(list(ln)) #, ln
