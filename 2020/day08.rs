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

fn onepass( data : Program ) -> Result<i32,i32> {
    let mut pc = 0_usize;
    let mut accum = 0;
    let mut seen = HashSet::<usize>::new();

    loop {
        if seen.contains( &pc )
        {
            return Ok(accum)
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
/*

def cycle(base):
    for i in range(len(base)):
        data = base[:]
        if data[i][0] == 'acc':
            continue
        if DEBUG:
            print( "Trying", i )
        if data[i][0] == 'nop':
            data[i] = ('jmp',data[i][1])
        elif data[i][0] == 'jmp':
            data[i] = ('nop',data[i][1])
        (res,val) = onepass(data)
        if res:
            print( "SUCCESS", val )
            return val
*/


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

    println!("{:?}", data );

    let val = onepass(data);
    println!( "Part 1: {}", val.unwrap() )

    /*
    let mut program = Vec::<Instruction>::new();
    for line in data {
        program.extend( parse_instruction(line) );
    }

    let final1 = program.iter().fold(initial_state, |pos,instr| eval1(pos,*instr));

    println!("Part 1: {:?}", mandist(final1) );

    let final2 = program.iter().fold(initial_state, |pos,instr| eval2(pos,*instr));

    println!("Part 2: {:?}", mandist(final2) );
    */
}
