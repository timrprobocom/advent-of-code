test = [
"1-3 a: abcde",
"1-3 b: cdefg",
"2-9 c: ccccccccc"
]

pat = r"(\d+)-(\d+) (.): (.*)$"

function pass1( line )
    (a, b, tgt, haystack) = match(pat, line).captures
    a = parse(Int32, a)
    b = parse(Int32, b)
    h = count(i->(i==only(tgt)), haystack)
    return a <= h  <= b
end

function pass2( line )
    (a, b, tgt, haystack) = match(pat, line).captures
    a = parse(Int32, a)
    b = parse(Int32, b)
    tgt = only(tgt)
    return (haystack[a] == tgt) != (haystack[b] == tgt)
end

live = readlines("day02.txt")

function evaluate( lines, passx )
    return sum( passx, lines )
end

println( "1: ", evaluate( test, pass1 ) )
println( "Part 1: ", evaluate( live, pass1 ) )
println( "2: ", evaluate( test, pass2 ) )
println( "Part 2: ", evaluate( live, pass2 ) )
