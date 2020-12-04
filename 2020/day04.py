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
iyr:2011 ecl:brn hgt:59in""".splitlines()

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
    data = test
else:
    # Tackily, we rely on the extra blank this generates.
    data = open('day04.txt').read().split('\n')


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

def validate(field,value):
    if DEBUG:
        print( "Checking", field, value )
    try:
        if field == 'byr':
            yr = int(value)
            return 1920 <= yr <= 2002
        if field == 'iyr':
            yr = int(value)
            return 2010 <= yr <= 2020
        if field == 'eyr':
            yr = int(value)
            return 2020 <= yr <= 2030
        if field == 'hgt':
            if value[-2:] == 'cm':
                val = int(value[:-2])
                return 150 <= val <= 193
            if value[-2:] == 'in':
                val = int(value[:-2])
                return 59 <= val <= 76
            return False
        if field == 'hcl':
            return re.fullmatch( r'#[0-9a-f]{6}', value )
        if field == 'ecl':
            return value in ('amb','blu','brn','gry','grn','hzl','oth')
        if field == 'pid':
            return re.fullmatch( '\d{9}', value )
        if field == 'cid':
            return True

    except ValueError:
        return False

    return False


def part2(data):
    count1 = 0
    count2 = 0
    keys = {'cid':0}
    for line in data:
        line = line.strip()
        if not line:
            fail = False
            if len(keys) != 8:
                if DEBUG:
                    print("FAIL not enough keys")
                fail = True
            else:
                count1 += 1
                for key,val in keys.items():
                    if not validate(key,val):
                        if DEBUG:
                            print( "FAIL", key, val )
                        fail = True
                        break
            if not fail:
                if DEBUG:
                    print("PASS")
                count2 += 1
            keys = {'cid': 0 }
        if DEBUG:
            print( line )
        for part in line.split():
            key,_,val = part.partition(':')
            keys[key] = val
    return (count1,count2)


p1,p2 = part2(data)
print( "Part 1: ", p1 )
print( "Part 2: ", p2 )


