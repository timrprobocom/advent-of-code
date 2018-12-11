
nums = open('day01.txt').readlines()
print len(nums)

def part1(nums):
    sum = 0
    for ln in nums:
        sum += int(ln)
    return sum

def part2(nums):
    cnts = set()
    sum = 0
    found = -1
    while found < 0:
        print '*',
        for ln in nums:
            sum += int(ln)
            if sum in cnts:
                found = sum
                break
            cnts.add(  sum  )
    print
    return found

print( part1(nums) )
print( part2(nums) )
