package main

import (
	"fmt"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

//go:embed day02.txt
var live string

// 1 rock X A
// 2 paper Y B
// 3 scissors Z C

// win lose draw +6 +0 +3

var test = `
A Y
B X
C Z`[1:]

var score = map[string]byte {
    "AX": 3,
    "BY": 3,
    "CZ": 3,
    "AY": 6,
    "BZ": 6,
    "CX": 6,
    "AZ": 0,
    "BX": 0,
    "CY": 0 }

// "ldw" which is XYZ
var need = map[byte]string {
    'A': "ZXY",
    'B': "XYZ",
    'C': "YZX" }


func part(data []string) (int,int) {
    count1 := 0
    count2 := 0
	for _, game := range(data) {
        mypick := game[2]
		both := string(game[0])+string(mypick)
        count1 += int(score[both] + mypick - 'W')
        choice := game[2] - 'X'
        mypick = need[game[0]][choice]
		both = string(game[0])+string(mypick)
        count2 += int(score[both] + mypick - 'W')
	}
    return count1,count2
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n")
	count1, count2 := part(data)

	fmt.Println("Part 1:", count1)
	fmt.Println("Part 2:", count2)
}
