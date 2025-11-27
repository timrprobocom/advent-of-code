import sys

tots = 0
blank = 0

for fn in sys.argv[1:]:
    for line in open(fn).read().splitlines():
        tots += 1
        if not line:
            blank += 1

print(blank,'blanks,',tots-blank,'code,',tots,'total')
