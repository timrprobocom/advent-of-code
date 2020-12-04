import sys
import re

test = """
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in"""

#byr (Birth Year)
#iyr (Issue Year)
#eyr (Expiration Year)
#hgt (Height)
#hcl (Hair Color)
#ecl (Eye Color)
#pid (Passport ID)
#cid (Country ID)

DEBUG = 'debug' in sys.argv

if 'test' in sys.argv:
    data = test.split('\n\n')
else:
    data = open('day04.txt').read().split('\n\n')


#byr (Birth Year) - four digits; at least 1920 and at most 2002.
#iyr (Issue Year) - four digits; at least 2010 and at most 2020.
#eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
#hgt (Height) - a number followed by either cm or in:
#  If cm, the number must be at least 150 and at most 193.
#  If in, the number must be at least 59 and at most 76.
#hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
#ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
#pid (Passport ID) - a nine-digit number, including leading zeroes.
#cid (Country ID) - ignored, missing or not.


digits4 = re.compile('\d{4}')
digits9 = re.compile('\d{9}')
color =  re.compile('#[0-9a-f]{6}')

must = set(('byr','iyr','eyr','hgt','hcl','ecl','pid'))

def part2(data):
    count1 = 0
    count2 = 0
    for record in data:
        keys = {}
        for part in record.split():
            key,_,val = part.partition(':')
            keys[key] = val
        if DEBUG:
            print( record )

        if all( k in keys for k in must ):
            count1 += 1
            if  digits4.fullmatch(keys['byr']) and 1920 <= int(keys['byr']) <= 2002 and \
                digits4.fullmatch(keys['iyr']) and 2010 <= int(keys['iyr']) <= 2020 and \
                digits4.fullmatch(keys['eyr']) and 2020 <= int(keys['eyr']) <= 2030 and \
                (keys['hgt'][-2:] == 'cm' and 150 <= int(keys['hgt'][:-2]) <= 193 or \
                 keys['hgt'][-2:] == 'in' and  59 <= int(keys['hgt'][:-2]) <=  76) and \
                color.fullmatch( keys['hcl'] ) and \
                keys['ecl'] in ('amb','blu','brn','gry','grn','hzl','oth') and \
                digits9.fullmatch( keys['pid'] ):
                count2 += 1

    return (count1,count2)

p1,p2 = part2(data)
print( "Part 1: ", p1 )
print( "Part 2: ", p2 )


