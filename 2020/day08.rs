use std::env;
use std::collections::HashSet;

static TEST1 : [&str; 9] =
[
"nop +0",
"acc +1",
"jmp +4",
"acc +3",
"jmp -3",
"acc -99",
"acc +1",
"jmp -4",
"acc +6"
];

static TEST2 : [&str; 9] =
[
"nop +0",
"acc +1",
"jmp +4",
"acc +3",
"jmp -3",
"acc -99",
"acc +1",
"jmp -4",
"acc +6"
];

type Program = Vec<(String,i32)>;

fn onepass( data : &Program ) -> Result<i32,i32> {
    let mut pc = 0_usize;
    let mut accum = 0;
    let mut seen = HashSet::<usize>::new();

    loop {
        if seen.contains( &pc )
        {
            return Err(accum)
        }
        seen.insert(pc);
        if pc == data.len()
        {
            return Ok(accum)
        }
        if pc > data.len()
        {
            return Err(accum)
        }
        let (opc,delta) = &data[pc];
        if opc == "acc" {
            accum += delta;
        } else if opc == "jmp" {
            pc = (pc as i32 + *delta - 1) as usize;
        }
        pc += 1
    }
}

fn twopass( base : &Program ) -> i32 {
    for i in 0..base.len() {
        let mut data = base.clone();

        let (opc,delta) = &data[i];

        match &opc[..] {
            "acc" => continue,
            "nop" => data[i] = ("jmp".to_string(),*delta),
            "jmp" => data[i] = ("nop".to_string(),*delta),
            _ => panic!()
        }

        let result = onepass(&data);

        if let Ok(val) = result {
            return val;
        }
    }
    0
}


fn import( s : String ) -> (String,i32) {
    let mut parts = s.split_whitespace();
    (
        parts.next().unwrap().to_string(),
        parts.next().unwrap().parse::<i32>().unwrap()
    )
}


pub fn main() {
    let _debug : bool = env::args().any(|x| x=="debug");

    let data : Program = if env::args().any(|x| x=="test")  {
        TEST1
            .iter()
            .map(|x| import(x.chars().collect()))
            .collect()
    } else if env::args().any(|x| x=="test2")  {
        TEST2
            .iter()
            .map(|x| import(x.chars().collect()))
            .collect()
    } else {
        include_str!("day08.txt")
            .lines()
            .map(|x| import(x.chars().collect()))
            .collect()
    };

    let val = onepass(&data);

    let ans = match val {
        Ok(v) => v,
        Err(v) => v
    };
    println!( "Part 1: {}", ans );

    let ans = twopass(&data);
    println!( "Part 2: {}", ans )
}
