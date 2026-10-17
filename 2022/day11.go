package main

import (
	"fmt"
	"sort"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

//go:embed day11.txt
var live string

var test = `
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1`[1:]


type Monkey struct {
	Divisor int
	Factor int
	Items []int
	Divisible int
	True int
	False int
	Operation func(int) int
	Inspected int
}

func makeMonkey() *Monkey {
	return &Monkey{
		Divisor: 3,
		Factor: 1,
        Items: []int{},
        Divisible: 0,
        True: 0,
        False: 0,
//        Operation: None
        Inspected: 0,
	}
}

var MonkeyDivisor int = 0
var MonkeyFactor int = 0

func (s *Monkey) Print() {
	fmt.Println( s.Items, s.Inspected )
}

// The parsing is the hardest part.

func createMonkeys(data []string, divisor int) []*Monkey {
    monkeys := []*Monkey{}
    factor := 1
    MonkeyDivisor = divisor
	monkey := &Monkey{}
	for _, line := range data {
        if len(line) == 0 {
			continue
		}
        parts := strings.Fields(line)
		if parts[0] == "Monkey" {
            monkey = &Monkey{}
            monkeys = append( monkeys, monkey )
		} else if parts[0] == "Starting" {
			for _, n := range parts[2:] {
				monkey.Items = append( monkey.Items, tools.StrToInt(n) )
			}
        } else if parts[0] == "Operation:" {
            if parts[4] == "+" {
                monkey.Operation = func(k int) int { return k+tools.StrToInt(parts[5]) }
            } else if parts[5] == "old" {
                monkey.Operation = func(k int) int { return k*k }
            } else {
                monkey.Operation = func(k int) int { return k*tools.StrToInt(parts[5]) }
			}
        } else if parts[0] == "Test:" {
            monkey.Divisible = tools.StrToInt(parts[3])
            factor *= monkey.Divisible
        } else if parts[0] == "If" && parts[1] == "true:" {
            monkey.True = tools.StrToInt(parts[5])
        } else if parts[0] == "If" && parts[1] == "false:" {
            monkey.False = tools.StrToInt(parts[5])
		}
	}
    MonkeyFactor = factor
    return monkeys
}

func do1round( monkeys []*Monkey) {
    for _,m := range monkeys {
        m.Inspected += len(m.Items)
        for len(m.Items) > 0 {
            worry := (m.Operation(m.Items[0]) / MonkeyDivisor) % MonkeyFactor
			m.Items = m.Items[1:]
            if worry % m.Divisible > 0 {
                monkeys[m.False].Items = append( monkeys[m.False].Items, worry)
            } else {
                monkeys[m.True].Items = append( monkeys[m.True].Items, worry)
			}
		}
	}
}


func part1(data []string, divisor int, count int) int {
    monkeys := createMonkeys(data, divisor)
	if DEBUG {
		for _,m := range monkeys {
			m.Print()
		}
	}
    for range count {
        do1round(monkeys)
	}
	allx := []int{}
	for _,m := range monkeys {
		allx = append(allx, m.Inspected)
	}
	sort.Ints( allx )
    return allx[len(allx)-2]*allx[len(allx)-1]
}


func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(input, "\n")

	fmt.Println("Part 1:", part1(data, 3, 20))
	fmt.Println("Part 2:", part1(data, 1, 10000))
}

