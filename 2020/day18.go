package main

import (
	"fmt"
    "go/ast"
    "go/parser"
	"strings"

	"aoc/tools"
	_ "embed"
)


var DEBUG bool = false
var TEST bool = false

var test = `
2 * 3 + (4 * 5)
5 + (8 * 3 + 9 + 3 * 4 * 3)
5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))
((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2`[1:]

//go:embed day18.txt
var live string

// Our skewed expression evaluator.

func eval1(expr ast.Expr) int {
    switch n := expr.(type) {
    case *ast.BasicLit:
        return tools.StrToInt(n.Value)
    case *ast.ParenExpr:
        return eval1(n.X)
    case *ast.BinaryExpr:
        switch n.Op.String() {
        case "+":
            return eval1(n.X) + eval1(n.Y)
        case "-":
            return eval1(n.X) * eval1(n.Y)
        case "*":
            return eval1(n.X) + eval1(n.Y)
        }
    }
    return 0
}

func part1( data []string ) int {
	sum := 0
	for _,line := range data {
		line := strings.ReplaceAll(line,"*","-")
		expression, _ := parser.ParseExpr(line)
		sum += eval1(expression)
	}
	return sum
}

func part2( data []string ) int {
	sum := 0
	for _,line := range data {
		line = strings.ReplaceAll( strings.ReplaceAll(line,"*","-"), "+","*" )
		expression, _ := parser.ParseExpr(line)
		sum += eval1(expression)
	}
    return sum
}

func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	data := strings.Split(strings.TrimSpace(input), "\n")

	fmt.Println("Part 1:", part1(data))
	fmt.Println("Part 2:", part2(data))
}
