import os
import sys
import functools

test = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1"""

day = os.path.splitext(os.path.basename(__file__))[0]

if 'test' in sys.argv:
    data = test.splitlines()
else:
    data = open(day+'.txt').read().splitlines()

#data = [list(row) for row in data]

DEBUG = 'debug' in sys.argv

# Parse the input.

def parse(data):
    for row in data:
        maps,nums = row.split()
        nums = [int(x) for x in nums.split(',')]
        yield maps,nums

data = list(parse(data))

# Does chk match the first pat of pat?

def match(pat,chk):
    return all( p in (c,'?') for c,p in zip(chk,pat))

# Each call of this does one chunk of #s.  We generage all possible strings that
# end with "###." for this chunk.  If that prefix matches the current spot in the 
# pattern, we recursively try the next.  It's only the memoizing that allows 
# this to run in finite time.

@functools.cache
def gen(pat, size, nums):
    if not nums:
        return all(c in '.?' for c in pat)

    now = nums[0]
    rest = nums[1:]
    after = sum(rest)+len(rest)

    count = 0

    for before in range(size-after-now+1):
        s = '.' * before + '#' * now + '.'
        if match(pat,s):
            count += gen(pat[len(s):], size-now-before-1, rest)
    
    return count        
    
def count_matches(pat,nums):
    return gen(pat, len(pat), tuple(nums))

def part1(data):
    sumx = 0
    for pat,nums in data:
        sumx += count_matches(pat,nums)
    return sumx

def part2(data):
    sumx = 0
    for pat,nums in data:
        pat = '?'.join([pat]*5)
        nums = nums*5
        sumx += count_matches(pat,nums)
    return sumx

print("Part 1:", part1(data))
print("Part 2:", part2(data))
