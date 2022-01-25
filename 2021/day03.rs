use std::env;


// Is it better to keep the input as a string, or as an integer?
// It's the difference between row[i] and row & bit.

fn common( data : &Vec<String> ) -> (u32, u32)
{
    // We need to enumerate vertically here.

    let num: usize = data.len();
    let bits: usize = data[0].len();
    let mut counts = vec![0; bits];

    for row in data {
        for (i,c) in row.char_indices() {
            if c == '1' {
                counts[i] += 1;
            }
        }
    }

    let mut res : u32 = 0;
    for i in counts
    {
        res = res * 2 + if i * 2 >= num { 1 } else { 0 };
    }

    let allone: u32 = (1 << bits) - 1;
    (res, allone-res)
}

fn part1( data: &Vec<String> ) -> u32
{
    let (most, least) = common(data);
    most * least
}

fn part2( data: &Vec<String> ) -> u32
{
    let bits: usize = data[0].len();
    let mut hdata = data.to_owned();
    let mut ldata = data.to_owned();

    for bitno in 0..bits {
        let bit = 1 << (bits-bitno-1);

        if hdata.len() > 1 {
            let (most,_least) = common(&hdata);
            let crit = if bit & most != 0 {'1'} else {'0'};
            hdata = hdata
                .into_iter()
                .filter(|row| row.chars().nth(bitno).unwrap() == crit)
                .collect();
        }

        if ldata.len() > 1 {
            let (_most,least) = common(&ldata);
            let crit = if bit & least != 0 {'1'} else {'0'};
            ldata = ldata
                .into_iter()
                .filter(|row| row.chars().nth(bitno).unwrap() == crit)
                .collect();
        }

        if hdata.len() == 1 && ldata.len() == 1 {
            break;
        }
    }

    println!("{} {}", hdata[0], ldata[0]);

    u32::from_str_radix(&hdata[0], 2).unwrap()
        *
    u32::from_str_radix(&ldata[0], 2).unwrap()
}



static TEST : [&str; 12] = 
[
    "00100",
    "11110",
    "10110",
    "10111",
    "10101",
    "01111",
    "00111",
    "11100",
    "10000",
    "11001",
    "00010",
    "01010"
];

pub fn main() {
    let live : Vec<String> = if env::args().any(|x| x == "test")
    {
        TEST
            .iter()
            .map(|x| x.to_string())
            .collect()
    } else {
        include_str!("day03.txt")
            .lines()
            .map(|x| x.to_string())
            .collect()
    };

    println!( "Pass 1: {}", part1( &live ));
    println!( "Pass 2: {}", part2( &live ));
}
