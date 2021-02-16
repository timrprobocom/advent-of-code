use regex::{Regex,Captures};
use lazy_static::lazy_static;

fn parse<'a>( caps : &'a Captures ) -> (usize, usize, char, &'a str) {
    (
        caps.get(1).unwrap().as_str().parse::<usize>().unwrap(),
        caps.get(2).unwrap().as_str().parse::<usize>().unwrap(),
        caps.get(3).unwrap().as_str().chars().next().unwrap(),
        caps.get(4).unwrap().as_str()
    )
}

fn pass1( a : usize, b : usize, tgt : char, hay : &str) -> bool {
    let cnt = hay.matches(tgt).count();
    a <= cnt && cnt <= b
}

fn pass2( a : usize, b : usize, tgt : char, hay0 : &str) -> bool {
    let hay : Vec<char> = hay0.chars().collect();
    (hay[a-1] == tgt) != (hay[b-1] == tgt)
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

    let live : Vec<Captures> = include_str!("../../day02.txt")
        .lines()
        .map(|line| MYRE.captures(line).unwrap())
        .collect();

    let part1 = live
        .iter()
        .map(|x| parse(x) )
        .filter(|(a,b,c,d)| pass1(*a,*b,*c,d) )
        .count();

    println!("Part 1: {}", part1 );

    let part2 = live
        .iter()
        .map(|x| parse(x) )
        .filter(|(a,b,c,d)| pass2(*a,*b,*c,d) )
        .count();

    println!("Part 2: {}", part2 );

    Ok(())
}
