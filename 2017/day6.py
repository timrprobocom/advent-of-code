
test = [0, 2, 7, 0]

live = [
    10, 3, 15, 10, 5, 15, 5, 15, 9, 2, 5, 8, 5, 2, 3, 6
]

blocks = live

def pass1( blocks ):
    mx = max(blocks)
    midx = blocks.index(mx)
    handout = blocks[midx]
    blocks[midx] = 0
    for i in range(handout):
        midx = (midx + 1) % len(blocks)
        blocks[midx] += 1

found = {}

passes = 0
while 1:
    print blocks
    b1 = tuple(blocks)
    if b1 in found:
        break
    found[b1] = passes
    pass1( blocks )
    passes += 1

print found[b1]
print passes
print passes - found[b1]

