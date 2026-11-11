open System.Text.RegularExpressions

let test = [|
    "1-3 a: abcde"
    "1-3 b: cdefg"
    "2-9 c: ccccccccc"
|]

let pat = Regex "(\d+)-(\d+) (.): (.*)$"
let mat = pat.Match test.[0]
printfn "%A" mat
printfn "%A" (int mat.Groups.[1].Value)
printfn "%A" (int mat.Groups.[2].Value)

type Problem = int * int * char * string

let parseLine (line: string): Problem =
    let mat = pat.Match line
    (int mat.Groups.[1].Value), (int mat.Groups.[2].Value), mat.Groups.[3].Value.[0], mat.Groups.[4].Value

//    mat.Groups |> fun word -> word.Value

printfn "%A" (parseLine test.[0])

let pass1 (prob: Problem): bool =
    let a,b,_,d = prob
    a <= d.Length && d.Length <= b

let p1 = test |> List.map (fun x -> parseLine x |> pass1)
printfn "%A" p1

// def pass1( line ):
//     a, b, tgt, haystack = pat.match(line).groups()
//     a, b = int(a), int(b)
//     return a <= haystack.count(tgt)  <= b
// 
// def pass2( line ):
//     a, b, tgt, haystack = pat.match(line).groups()
//     a, b = int(a), int(b)
//     return (haystack[a-1] == tgt) != (haystack[b-1] == tgt)
// 
// live = open('day02.txt').readlines()
// 
// def evaluate( lines, passx ):
//     return sum( passx(line) for line in lines )
// 
// print( "2:", evaluate( test, pass1 ) )
// print( "Part 1:", evaluate( live, pass1 ) )
// print( "1:", evaluate( test, pass2 ) )
// print( "Part 2:", evaluate( live, pass2 ) )
