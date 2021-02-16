use regex::{Regex,Captures};
use lazy_static::lazy_static;

fn parse<'a>( caps : &'a Captures ) -> (usize, usize, &'a str, &'a str) {
    let a = caps.get(1).unwrap().as_str().parse::<usize>().unwrap();
    let b = caps.get(2).unwrap().as_str().parse::<usize>().unwrap();
    let tgt = caps.get(3).unwrap().as_str();
    let hay = caps.get(4).unwrap().as_str();
    (a, b, tgt, hay)
}

fn pass1( caps : &Captures ) -> bool {
    let a = caps.get(1).unwrap().as_str().parse::<usize>().unwrap();
    let b = caps.get(2).unwrap().as_str().parse::<usize>().unwrap();
    let tgt = caps.get(3).unwrap().as_str();
    let hay = caps.get(4).unwrap().as_str();
//fn pass1( a : usize, b : usize, tgt : &str, hay : &str) -> bool {
    let cnt = hay.matches(tgt).count();
    a <= cnt && cnt <= b
}

fn pass2( caps : &Captures ) -> bool {
    let a = caps.get(1).unwrap().as_str().parse::<usize>().unwrap();
    let b = caps.get(2).unwrap().as_str().parse::<usize>().unwrap();
    let tgt = caps.get(3).unwrap().as_str().chars().next().unwrap();
    let hay : Vec<char> = caps.get(4).unwrap().as_str().chars().collect();
    (hay[a-1] == tgt) != (hay[b-1] == tgt)
}

fn main() -> std::io::Result<()> {

    let _test = vec![
        "1-3 a: abcde",
        "1-3 b: cdefg",
        "2-9 c: ccccccccc"
    ];

    lazy_static! {
        static ref MYRE : Regex = Regex::new( 
            r"(\d+)-(\d+) (.): (.*)$"
        ).unwrap();
    }

    let part1 = include_str!("../../day02.txt")
        .lines()
        .map(|line| MYRE.captures(line).unwrap())
        .filter(|x| pass1(x) )
        .count();

    println!("Part 1: {}", part1 );

    let part2 = include_str!("../../day02.txt")
        .lines()
        .map(|line| MYRE.captures(line).unwrap())
        .filter(|x| pass2(x) )
        .count();

    println!("Part 2: {}", part2 );

    Ok(())
}
