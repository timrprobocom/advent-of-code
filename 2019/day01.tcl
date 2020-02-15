#! /usr/bin/tclsh

proc fuel1 mass {
    return [ expr { $mass / 3 - 2 } ]
}

proc fuel2 {mass sum} {
    set f [ fuel1 $mass ]
    if { $f <= 0 } { return $sum }
    return [ fuel2 $f [ expr { $sum+$f } ] ]
}

foreach test { 12 14 1969 100756 } {
    puts [ fuel2 $test 0 ]
}

set sum 0

set fp [open "day01.txt" r]
while { -1 != [gets $fp line] } {
    set sum [expr { $sum + [fuel2 $line 0] } ]
}
puts $sum



