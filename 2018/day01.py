import sys

DEBUG = 'debug' in sys.argv

nums = open('day01.txt').readlines()

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
        for ln in nums:
            sum += int(ln)
            if sum in cnts:
                found = sum
                break
            cnts.add(  sum  )
    return found

print( "Part 1:", part1(nums) )
print( "Part 2:", part2(nums) )
