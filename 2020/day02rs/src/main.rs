use regex::{Regex,Captures};
use lazy_static::lazy_static;

struct Problem {
    a: usize,
    b: usize,
    tgt: char,
    hay: String
}

fn parse( caps : &Captures ) -> Problem {
    Problem {
        a:   caps.get(1).unwrap().as_str().parse::<usize>().unwrap(),
        b:   caps.get(2).unwrap().as_str().parse::<usize>().unwrap(),
        tgt: caps.get(3).unwrap().as_str().chars().next().unwrap(),
        hay: caps.get(4).unwrap().as_str().to_string()
    }
}

fn pass1( p : &Problem ) -> bool {
    let cnt = p.hay.matches(p.tgt).count();
    p.a <= cnt && cnt <= p.b
}

fn pass2( p : &Problem ) -> bool {
    let hay : Vec<char> = p.hay.chars().collect();
    (hay[p.a-1] == p.tgt) != (hay[p.b-1] == p.tgt)
}

fn main() -> std::io::Result<()> {

/*
    let _test = vec![
        "1-3 a: abcde",
        "1-3 b: cdefg",
        "2-9 c: ccccccccc"
    ];
*/

    lazy_static! {
        static ref MYRE : Regex = Regex::new( 
            r"(\d+)-(\d+) (.): (.*)$"
        ).unwrap();
    }

    let live : Vec<Problem> = include_str!("../../day02.txt")
        .lines()
        .map(|line| MYRE.captures(line).unwrap())
        .map(|x| parse(&x) )
        .collect();

    let part1 = live
        .iter()
        .filter(|x| pass1(x) )
        .count();

    println!("Part 1: {}", part1 );

    let part2 = live
        .iter()
        .filter(|x| pass2(x) )
        .count();

    println!("Part 2: {}", part2 );

    Ok(())
}
