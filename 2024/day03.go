package main

import (
    "fmt"
)

import _ "embed"

import "aoc/tools"

var DEBUG bool = false
var TEST bool = false

var test = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"

//go:embed day03.txt
var live string

func is_safe( row []int ) bool {
    for i := 0; i < len(row)-1; i++ {
        x := row[i]
        y := row[i+1]
        if (y-x) * (row[1]-row[0]) < 0 {
            return false
        }
        if tools.AbsInt(y-x) < 1 || tools.AbsInt(y-x) > 3 {
            return false
        }
    }
    return true
}

func part1( data string ) int {
    sumx := 0
    for i := 0; i < len(data)-4; i++ {
        if data[i:i+4] == "mul(" {
            i += 4
            a, b := 0, 0
            for ; tools.Isdigit(data[i]); i++  {
                a = a * 10 + int(data[i]) - '0'
            }
            if data[i] != ',' {
                continue
            }
            for i++; tools.Isdigit(data[i]); i++  {
                b = b * 10 + int(data[i]) - '0'
            }
            if data[i] != ')' {
                continue
            }
            sumx += a * b
        }
    }
    return sumx
}

// These could be combined by adding "if part == 2 && data[i:i+4] == "do()".

func part2( data string ) int {
    sumx := 0
    yes := true
    for i := 0; i < len(data)-4; i++ {
        if data[i:i+4] == "do()" {
            yes = true
        } else if i+7 < len(data) && data[i:i+7] == "don't()" {
            yes = false
        } else if yes && data[i:i+4] == "mul(" {
            i += 4
            a, b := 0, 0
            for ; tools.Isdigit(data[i]); i++  {
                a = a * 10 + int(data[i]) - '0'
            }
            if data[i] != ',' {
                continue
            }
            for i++; tools.Isdigit(data[i]); i++  {
                b = b * 10 + int(data[i]) - '0'
            }
            if data[i] != ')' {
                continue
            }
            sumx += a * b
        }
    }
    return sumx;
}


func main() {
    var input string
    TEST, DEBUG, input = tools.Setup( test, live )

    fmt.Println("Part 1:", part1(input))
    fmt.Println("Part 2:", part2(input))
}

