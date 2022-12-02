use std::env;

struct Position {
    pos : i32,
    depth : i32,
    aim : i32,
}

#[allow(dead_code)]
impl Position {
    fn repr(&self) -> String {
        return format!("<Position {} {} {}", self.pos, self.depth, self.aim)
    }
}

struct Command {
    verb: String,
    count: i32
}

// Parse the directions.

fn parse( data: &Vec<String> ) -> Vec<Command>
{
    data.iter()
        .map(|ln| ln.trim_end_matches('\n').split_whitespace())
        .map(|mut parts| Command{ 
            verb: parts.next().unwrap().to_string(),
            count: parts.next().unwrap().parse::<i32>().unwrap() 
        })
        .collect()
}

fn part1( cmds: &Vec<Command> ) -> i32
{
    let mut pos = Position{ pos: 0, depth: 0, aim: 0 };
    for cmd in cmds
    {
        match cmd.verb.as_str() {
            "forward" => pos.pos += cmd.count,
            "up"      => pos.depth -= cmd.count,
            "down"    => pos.depth += cmd.count,
            _         => ()
        }
    }
    return pos.pos * pos.depth
}


fn part2( cmds: &Vec<Command> ) -> i32
{
    let mut pos = Position{ pos: 0, depth: 0, aim: 0 };
    for cmd in cmds
    {
        match cmd.verb.as_str() {
            "forward" => { 
                pos.pos += cmd.count;
                pos.depth += pos.aim * cmd.count 
            },
            "up"      => pos.aim -= cmd.count,
            "down"    => pos.aim += cmd.count,
            _         => ()
        }
    }
    return pos.pos * pos.depth
}

static TEST : [&str; 6] = 
[
    "forward 5",
    "down 5",
    "forward 8",
    "up 3",
    "down 8",
    "forward 2"
];

pub fn main() {
    let live : Vec<String> = if env::args().any(|x| x == "test")
    {
        TEST
            .iter()
            .map(|x| x.to_string())
            .collect()
    } else {
        include_str!("day02.txt")
            .lines()
            .map(|x| x.to_string())
            .collect()
    };

    println!( "Pass 1: {}", part1( &parse( &live ) ));
    println!( "Pass 2: {}", part2( &parse( &live ) ));
}
