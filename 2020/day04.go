package main

import (
	"fmt"
	"regexp"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false
var test = `
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in`[1:]

//byr (Birth Year)
//iyr (Issue Year)
//eyr (Expiration Year)
//hgt (Height)
//hcl (Hair Color)
//ecl (Eye Color)
//pid (Passport ID)
//cid (Country ID)

//go:embed day04.txt
var live string



//byr (Birth Year) - four digits; at least 1920 and at most 2002.
//iyr (Issue Year) - four digits; at least 2010 and at most 2020.
//eyr (Expiration Year) - four digits; at least 2020 and at most 2030.
//hgt (Height) - a number followed by either cm or in:
//  If cm, the number must be at least 150 and at most 193.
//  If in, the number must be at least 59 and at most 76.
//hcl (Hair Color) - a # followed by exactly six characters 0-9 or a-f.
//ecl (Eye Color) - exactly one of: amb blu brn gry grn hzl oth.
//pid (Passport ID) - a nine-digit number, including leading zeroes.
//cid (Country ID) - ignored, missing or not.


var digits4 = regexp.MustCompile(`^\d{4}$`)
var digits9 = regexp.MustCompile(`^\d{9}$`)
var color = regexp.MustCompile(`^#[0-9a-f]{6}$`)

var must = []string{"byr","iyr","eyr","hgt","hcl","ecl","pid"}
var eyecolor = map[string]int8{"amb":1,"blu":1,"brn":1,"gry":1,"grn":1,"hzl":1,"oth":1}

func part2(data []string) (int, int) {
    count1 := 0
    count2 := 0
    for _,record := range data {
        keys := make(map[string]string)
		for _,part := range strings.Fields(record) {
			i := strings.Index(part, ":")
			key := part[:i]
			val := part[i+1:]
            keys[key] = val
		}
        if DEBUG {
            fmt.Println( keys )
		}

		allok := true
        for _,m := range must {
			_,ok := keys[m]
			allok = allok && ok
			if ! ok {
				break
			}
		}

		if allok {
			count1++

			hgt := keys["hgt"]
			hgtunit := hgt[len(hgt)-2:]
			hgtval := hgt[:len(hgt)-2]

            if  digits4.MatchString(keys["byr"]) && tools.Within( 1920, tools.StrToInt(keys["byr"]), 2002) &&
                digits4.MatchString(keys["iyr"]) && tools.Within( 2010, tools.StrToInt(keys["iyr"]), 2020) &&
                digits4.MatchString(keys["eyr"]) && tools.Within( 2020, tools.StrToInt(keys["eyr"]), 2030) &&
                (hgtunit == "cm" && tools.Within(150, tools.StrToInt(hgtval), 193) ||
                 hgtunit == "in" && tools.Within( 59, tools.StrToInt(hgtval), 76)) &&
                color.MatchString( keys["hcl"] ) &&
                eyecolor[keys["ecl"]] == 1 &&
                digits9.MatchString( keys["pid"] ) {
                count2 ++
			}
		}
	}

    return count1, count2
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n\n")

    p1, p2 := part2(data)
	fmt.Println("Part 1:", p1)
	fmt.Println("Part 2:", p2)
}
