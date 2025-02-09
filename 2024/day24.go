package main

import (
	"fmt"
	"slices"
	"strings"

	"aoc/tools"
	_ "embed"
)

var DEBUG bool = false
var TEST bool = false

var test string = `
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj`[1:]

//go:embed day24.txt
var live string

type Gates map[string]int16
type Rules [][]string

func operate(gates Gates, a string, op string, b string) int16 {
	switch op {
	case "AND":
		return gates[a] & gates[b]
	case "OR":
		return gates[a] | gates[b]
	case "XOR":
		return gates[a] ^ gates[b]
	}
	return 0
}

func binary(gates Gates, c byte) int64 {
	var sum int64 = 0
	for k, v := range gates {
		if k[0] == c {
			n := tools.StrToInt(k[1:])
			sum |= int64(v) << n
		}
	}
	return sum
}

func printrow(sv []string, sep string) string {
	var s string
	for _, psv := range sv {
		if len(s) > 0 {
			s += sep
		}
		s += psv
	}
	return s
}

func do_a_run(gates Gates, incodes Rules, swap map[string]string) int64 {
	xgates := make(Gates)
	for k, v := range gates {
		if k[0] == 'x' || k[0] == 'y' {
			xgates[k] = v
		}
	}

	codes := incodes
	for len(codes) > 0 {
		var undone Rules
		for _, row := range codes {
			a := row[0]
			op := row[1]
			b := row[2]
			r := row[4]

			_, ok1 := xgates[a]
			_, ok2 := xgates[b]
			if ok1 && ok2 {
				if swap[r] != "" {
					r = swap[r]
				}
				xgates[r] = operate(xgates, a, op, b)
			} else {
				undone = append(undone, row)
			}
		}
		if len(undone) == len(codes) {
			return -1
		}

		codes = undone
	}
	return binary(xgates, 'z')
}

// Parse the rules.

// Xn XOR Yn => Mn
// Xn AND Yn => Nn
// Cn-1 AND Mn => Rn
// Cn-1 XOR Mn -> Zn
// Rn OR Nn -> Cn

var swaps []string

func part1(gates Gates, incodes Rules) int64 {
	var zs []string
	for _, rule := range incodes {
		if rule[4][0] == 'z' {
			zs = append(zs, rule[4])
		}
	}
	slices.Sort(zs)

	// Make our expectations.

	lastcarry := "xxx"
	outgates := make(Gates)
	xgates := make(Gates)
	codes := slices.Clone(incodes)

	// For all the Zs (that is, all the outputs)...
	for _, rzv := range zs {
		x := "x" + rzv[1:]
		y := "y" + rzv[1:]

		// sources holds the signals we already know by now.
		sources := make(map[string]bool)
		sources[x] = true
		sources[y] = true

		xgates[x] = gates[x]
		xgates[y] = gates[y]

		// new_rules is used to construct a printable representation of the rules.
		new_rules := tools.Repeat([]string{"   ", "   ", "   ", "  ", "   "}, 5)
		for len(codes) > 0 {
			var undone Rules
			for _, rule := range codes {
				c1 := rule[0]
				op := rule[1]
				c2 := rule[2]
				r := rule[4]

				_, ok1 := xgates[c1]
				_, ok2 := xgates[c2]
				if ok1 && ok2 {
					switch op {
					case "AND":
						xgates[r] = xgates[c1] & xgates[c2]
						if sources[c1] && sources[c2] {
							new_rules[3] = rule
						} else {
							new_rules[2] = rule
						}
					case "OR":
						xgates[r] = xgates[c1] | xgates[c2]
						new_rules[4] = rule
					case "XOR":
						xgates[r] = xgates[c1] ^ xgates[c2]
						if sources[c1] && sources[c2] {
							new_rules[0] = rule
						} else {
							new_rules[1] = rule
						}
					}
				} else {
					undone = append(undone, rule)
				}
			}
			if len(undone) == len(codes) {
				break
			}
			codes = undone
		}

		// Capture the output.

		outgates[rzv] = xgates[rzv]

		if DEBUG {
			for _, row := range new_rules {
				fmt.Print(printrow(row, " "), "   ")
			}
			fmt.Println()
		}

		// Validate the rules to find the bugs.

		if new_rules[1][0] != "   " {
			if new_rules[1][4][0] != 'z' {
				if DEBUG {
					fmt.Println("WRONG", printrow(new_rules[1], " "), "swap", rzv, "and", new_rules[1][4])
				}
				swaps = append(swaps, rzv)
				swaps = append(swaps, new_rules[1][4])
			}
			if !slices.Contains(new_rules[1], new_rules[0][4]) {
				shd := "???"
				if new_rules[1][0] == lastcarry {
					shd = new_rules[1][2]
				} else {
					shd = new_rules[1][0]
				}
				if DEBUG {
					fmt.Println("WRONG", new_rules[0][4], "not present in", printrow(new_rules[1], " "), "swap", new_rules[0][4], " ", shd)
				}
				swaps = append(swaps, new_rules[0][4])
				swaps = append(swaps, shd)
			}
		}
		if new_rules[4][4] != "   " {
			lastcarry = new_rules[4][4]
		}
	}
	return binary(outgates, 'z')
}

// This just validates the swaps.

func validate(gates Gates, codes Rules) bool {
	xx := binary(gates, 'x')
	yy := binary(gates, 'y')
	target := xx + yy

	swapmap := make(map[string]string)
	for i := 0; i < len(swaps); i += 2 {
		swapmap[swaps[i]] = swaps[i+1]
		swapmap[swaps[i+1]] = swaps[i]
	}
	fmt.Println(len(gates), len(codes), len(swapmap))
	ans := do_a_run(gates, codes, swapmap)
	if DEBUG {
		fmt.Println(target, "==?", ans)
	}
	return target == ans
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)

	gates := make(Gates)
	var codes Rules

	for _, line := range strings.Split(input, "\n") {
		if len(line) > 0 {
			if line[3] == ':' {
				gates[line[:3]] = int16(line[5] - '0')
			} else {
				codes = append(codes, strings.Split(line, " "))
			}
		}
	}

	fmt.Println("Part 1:", part1(gates, codes))
	if DEBUG && !TEST {
		fmt.Println("Validate: ", validate(gates, codes))
	}
	if !TEST {
		slices.Sort(swaps)
		fmt.Println("Part 2:", printrow(swaps, ","))
	}
}
