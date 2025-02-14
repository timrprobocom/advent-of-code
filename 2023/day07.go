package main

import (
	"fmt"
	"strings"
	"slices"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false
var test = `
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483`[1:]

var order string = "23456789TJQKA"

//go:embed day07.txt
var live string

func counter( s string ) map[rune]int {
	cts := make(map[rune]int)
	for _, c := range s {
		cts[c]++
	}
	return cts
}

type Count struct {
	c rune
	n int
}

func reversecount( m map[rune]int ) []Count {
	counts := []Count{}
	for k,v := range m {
		counts = append( counts, Count{k,v} )
	}
	slices.SortFunc( counts, func( a,b Count ) int {
		return b.n - a.n
	})
	return counts
}


//6 Five of a kind, where all five cards have the same label: AAAAA
//5 Four of a kind, where four cards have the same label and one card has a different label: AA8AA
//4 Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
//3 Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
//2 Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
//1 One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
//0 High card, where all cards' labels are distinct: 23456

func grade ( hand string ) int {
	value := 0
	for _, c := range hand {
		value = value * 15 + strings.IndexRune(order, c)
	}

	cts := counter(hand)

    // For pass 2, replace the joker by the most common card.

    if order[0] == 'J' && cts['J'] > 0 {
        pick := 'J'
		for chk := 5; pick == 'J' && chk > 0; chk-- {
			for k,v := range cts {
				if v == chk && k != 'J' {
					pick = k
					break
				}
			}
		}

        hand = strings.Replace(hand,"J",string(pick),-1)
        cts = counter(hand)
	}

    vals := reversecount( cts )
	if DEBUG {
		fmt.Println(vals)
	}

    switch len(vals) {
		case 1:
		    value += 60000000
		case 2:
			if vals[0].n == 4 {
				value += 50000000
			} else {
				value += 40000000
			}
		case 3:
			if vals[0].n == 3 {
				value += 30000000
			} else {
				value += 20000000
			}
		case 4:
			value += 10000000
	}
	return value
}

type Hand struct {
	score int
	hand string
	bid int
}

func part1( data []string ) int {
   hands := []Hand{}
   for _, row := range data {
       hand,bid,_ := strings.Cut(row, " ")
       score := grade(hand)
       hands = append(hands, Hand{score,hand,tools.StrToInt(bid)} )
	   slices.SortFunc( hands, func (a, b Hand) int {
		   return a.score - b.score
	   })
   }
   sum := 0
   for n,h := range hands {
	   if DEBUG {
		   fmt.Println( n+1, h.hand, h.score, (n+1 * h.bid ) )
	   }
	   sum += (n+1) * h.bid
   }
   return sum
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n")

	fmt.Println("Part 1:", part1(data))
	order = "J23456789TQKA"
	fmt.Println("Part 2:", part1(data))
}




