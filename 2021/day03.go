package main

import (
	"fmt"
	"strconv"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test = `
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010`[1:]

//go:embed day03.txt
var live string


func common( data []string ) (int,int) {
    num := len(data)
    bits := len(data[0])
    allone := (1 << bits) - 1
	counts := make([]int, bits)

    for _,row := range data {
        for i,c := range row {
			if c == '1' {
				counts[i] ++
			}
		}
	}

    res := 0
    for _,i := range counts {
		res *= 2
		if i*2 >= num {
			res ++
		}
	}
    if DEBUG {
        fmt.Println(num, bits, counts, res)
	}
    return res, allone-res
}

func part1(data []string) int {
	most, least := common(data)
	return most * least
}


func part2(data []string) int {
    bits := len(data[0])

    hdata := data
    ldata := data

    for bitno := range(bits) {
		bitn := bits-bitno-1
        if len(hdata) > 1 {
            most, _ := common(hdata)
			crit := "01"[(most>>bitn) & 1]
			newhdata := []string{}
			for _,row := range hdata {
				if row[bitno] == crit {
					newhdata = append(newhdata, row)
				}
			}
			hdata = newhdata
		}

        if len(ldata) > 1 {
            _, least := common(ldata)
			crit := "01"[(least>>bitn) & 1]
			newldata := []string{}
			for _,row := range ldata {
				if row[bitno] == crit {
					newldata = append(newldata, row)
				}
			}
			ldata = newldata
		}

        if len(hdata) == 1 && len(ldata) == 1 {
            break
		}
	}

	if DEBUG {
		fmt.Println(hdata, ldata)
	}
	n1,_ := strconv.ParseInt(hdata[0],2,32)
	n2,_ := strconv.ParseInt(ldata[0],2,32)
    return int(n1*n2)
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input,"\n")

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}



