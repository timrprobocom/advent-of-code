import sys

dprint = print if 'debug' in sys.argv else lambda *s : None

def makerules():
    rules = {}
    for rule in open("day07.txt"):
        parts = rule.split();
        end = parts[-1]
        if parts[0] == "NOT":
            rules[end] = parts[:2]
        elif parts[1] == "AND":
            rules[end] = ("AND",parts[0],parts[2])
        elif parts[1] == "OR":
            rules[end] = ("OR",parts[0],parts[2])
        elif parts[1] == "LSHIFT":
            rules[end] = ("LSHIFT",parts[0],parts[2])
        elif parts[1] == "RSHIFT":
            rules[end] = ("RSHIFT",parts[0],parts[2])
        else:
            rules[end] = parts[0]
    return rules

def evaluate(n):
    if n.isnumeric():
        return int(n)
    coding = rules[n]
    dprint("IN:",n,coding)
    if isinstance(coding,int):
        return coding
    elif isinstance(coding,str):
        res = evaluate(coding)
    elif coding[0] == "NOT":
        res = evaluate(coding[1]) ^ 0xffff
    elif coding[0] == "AND":
        res = evaluate(coding[1]) & evaluate(coding[2])
    elif coding[0] == "OR":
        res = evaluate(coding[1]) | evaluate(coding[2])
    elif coding[0] == "LSHIFT":
        res = evaluate(coding[1]) << evaluate(coding[2])
    elif coding[0] == "RSHIFT":
        res = evaluate(coding[1]) >> evaluate(coding[2])
    rules[n] = res
    dprint( "OUT:", n, res )
    return res

rules = makerules()
parta = evaluate('a')
print( "Part 1:", parta )

rules = makerules()
rules['b'] = parta
print( "Part 2:", evaluate('a') )
