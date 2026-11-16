package main

import (
	"cmp"
	"fmt"
	"slices"
	"strings"

	"aoc/tools"
	_ "embed"
)


var DEBUG bool = false
var TEST bool = false
var dprint = tools.Absorb

var test = `
mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)`[1:]

//go:embed day21.txt
var live string

type Recipe struct {
	left []string
	right []string
}

// Each ingredient contains 0 or 1 allergens.
// Each allergen is in exactly 1 ingredient.

func parse(data []string) []Recipe {
	out := []Recipe{}
    for _,ln := range data {
        a,b,_ := strings.Cut(ln, " (contains ")
		out = append(out, Recipe{
			strings.Fields(a),
			strings.Split(b[:len(b)-1], ", "),
		})
	}
	return out
}


func process(data []string) (int,string) {

    // Ingredients contains each ingredient with a count of occurrences.

    ingredients := make(map[string]int)

    // Allergens contains each allergen with a set of the ingredients 
    // that might contain it.

    allergenx := make(map[string]map[string]bool)
    for _, recipe := range parse(data) {
		found := make(map[string]bool)
        for _,i := range recipe.left {
            ingredients[i]++
			found[i] = true
		}
        for _,i := range recipe.right {
			exist,ok := allergenx[i]
            if ! ok {
                allergenx[i] = found
            } else {
                allergenx[i] = tools.Intersect(exist, found)
			}
		}
	}

    dprint( ingredients )
    dprint( allergenx )

    // This is the list of all ingredients that might contain an allergen.

	allergens := make(map[string][]string)
    for k,v := range allergenx {
        allergens[k] = tools.Keys(v)
	}

	part1 := 0
	{
		known := make(map[string]bool)
		for _,v := range allergens {
			for _,k := range v {
				known[k] = true
			}
		}

		for k,v := range ingredients {
			if !known[k] {
				part1 += v
			}
		}
	}

    // Isolate the allergens which have only one possible ingredient.

    known := [][]string{}
	klist := make(map[string]bool)
    for true {

        // Find any entries that are down to one ingredient.

		singles := []string{}
		for k,v := range allergens {
			if len(v) == 1 {
				singles = append(singles, k)
			}
		}
        if len(singles) == 0 {
            break
		}

        for _,k := range singles {
			known = append( known, []string{k,allergens[k][0]} )
			klist[allergens[k][0]] = true
		}

        // Remove the singles from the remaining allergen list.

        for k,v := range allergens {
			newv := []string{}
			for _,vv := range v {
				if !klist[vv] {
					newv = append(newv, vv)
				}
			}
			allergens[k] = newv
		}
	}

    // Combine the ingredients, sorted by their allergens.

	slices.SortFunc(known, func(a, b []string) int { return cmp.Compare(a[0],b[0]) } )
    dprint( known )

	ilist := []string{}
	for _,k := range known {
		ilist = append(ilist, k[1])
	}
	mylist := strings.Join(ilist, ",")
    
    return part1, mylist
}



func main() {
	var input string
	TEST, DEBUG, input = tools.Setup(test, live)
	if DEBUG {
		dprint = fmt.Println
	}
	data := strings.Split(strings.TrimSpace(input), "\n")

	p1, p2 := process(data)
	fmt.Println("Part 1:", p1)
	fmt.Println("Part 2:", p2)
}

