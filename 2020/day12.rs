use std::env;

static TEST : [&str; 5] = 
[
    "F10",
    "N3",
    "F7",
    "R90",
    "F11"
];

// X is positive to the right (east).
// Y is positive to the bottom (south), like OS/2 but not Windows.

type Position = (i32,i32);

#[derive(Copy,Clone)]
enum Direction { 
    North, East, South, West
}

#[derive(Copy,Clone)]
enum Instruction {
  // Advance a number of steps
  Advance( i32 ),
  // Rotate 90 degrees clockwise
  Rotate,
  /// Advance steps in this direction
  AdvanceIn( i32, Direction )
}

// Retrieve a list of instructions from the given input string.
// `R180` would result in [Rotate; Rotate]
// `L90` would result in [Rotate; Rotate; Rotate]
fn parse_instruction (instruction: String) -> Vec<Instruction> {
    let count = instruction[1..].parse::<i32>().unwrap();
    match instruction.chars().next().unwrap() {
        'F' => vec![Instruction::Advance ( count ) ],
        'R' => vec![Instruction::Rotate ; (count / 90) as usize],
        'L' => vec![Instruction::Rotate ; ((360 - count) / 90) as usize],
        'N' => vec![Instruction::AdvanceIn ( count, Direction::North )],
        'E' => vec![Instruction::AdvanceIn ( count, Direction::East )],
        'W' => vec![Instruction::AdvanceIn ( count, Direction::West )],
        'S' => vec![Instruction::AdvanceIn ( count, Direction::South )],
        _  => vec![]
    }
}

// Retrieve a new position by moving `n` steps in a given direction from a 
// given position
fn movepos (n: i32, direction: &Direction, pos: Position) -> Position {
    let (x,y) = pos;
    match direction {
        Direction::North => (x, y - n),
        Direction::East => (x + n, y),
        Direction::South => (x, y + n),
        Direction::West => (x - n, y)
    }
}

// Retrieve a new direction by rotating 90 degrees clockwise from a given direction
fn rotate (direction: Direction) -> Direction {
    match direction {
        Direction::North => Direction::East,
        Direction::East => Direction::South,
        Direction::South => Direction::West,
        Direction::West => Direction::North
    }
}

// Rotate the position clockwise 90 degrees.
fn rotate_pt(point: Position) -> Position {
    (-point.1, point.0)
}

fn movewaypt(steps: i32, waypt: &Position, point: Position) -> Position {
    (point.0 + waypt.0 * steps, point.1 + waypt.1 * steps)
}

type State = (Position, Position, Direction);

// Create a new state by applying the given instruction to the given state.
// Waypoint is ignored.

fn eval1 ((position, waypt, direction): State, instruction: Instruction) -> State {
    match instruction {
        // When advancing, the position changes and the direction stays the same
        Instruction::Advance(steps) => (movepos( steps, &direction, position ), waypt, direction),
        Instruction::AdvanceIn(steps, thisdirection) => (movepos( steps, &thisdirection, position ), waypt, direction),
        // When rotating, the position stays the same and the direction changes
        Instruction::Rotate => (position, waypt, rotate(direction))
    }
}

// Create a new state by applying the given instruction to the given state.
// Direction is ignored.

fn eval2 ((position, waypt, direction): State, instruction: Instruction) -> State {
    let i =
    match instruction {
        Instruction::Advance(steps) => (movewaypt( steps, &waypt, position ), waypt, direction),
        Instruction::AdvanceIn(steps, thisdirection) => (position, movepos( steps, &thisdirection, waypt ), direction),
        Instruction::Rotate => (position, rotate_pt(waypt), direction)
    }; println!( "{:?} {:?}", i.0, i.1 ); i
}

fn mandist (state: State) -> i32 {
    let (x,y) = state.0;
    x.abs() + y.abs()
}


pub fn main() {
    let _debug : bool = env::args().any(|x| x=="debug");

    let data : Vec<String> = if env::args().any(|x| x=="test")  {
        TEST
            .iter()
            .map(|x| x.to_string())
            .collect()
    } else {
        include_str!("day12.txt")
            .lines()
            .map(|x| x.to_string())
            .collect()
    };

    let initial_state: State = ((0, 0), (10, -1), Direction::East);

    let mut program = Vec::<Instruction>::new();
    for line in data {
        program.extend( parse_instruction(line) );
    }

    let final1 = program.iter().fold(initial_state, |pos,instr| eval1(pos,*instr));

    println!("Part 1: {:?}", mandist(final1) );

    let final2 = program.iter().fold(initial_state, |pos,instr| eval2(pos,*instr));

    println!("Part 2: {:?}", mandist(final2) );
}
