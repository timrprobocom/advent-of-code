
fn generate ( dx: usize, dy: usize, limx: usize, limy: usize ) -> Vec<(usize,usize)> {
    let mut x : usize = 0;
    let mut y : usize = 0;
    let mut coords = Vec::<(usize,usize)>::new();
    while y < limy {
        coords.push( (x,y) );
        x = (x + dx) % limx;
        y += dy
    }
    coords
}

fn import ( incoming : Vec::<&str> ) -> Vec<Vec<char>> {
    incoming
        .iter()
        .map(|x| x.chars().collect())
        .collect()
}

fn counttrees( grid : &Vec<Vec<char>>, dx: usize, dy: usize ) -> usize {
    generate( dx, dy, grid[0].len(), grid.len() )
        .iter()
        .filter(|(x,y)| grid[*y][*x] == '#')
        .count()
}

pub fn main() {
    let _test = import( vec![
        "..##.......",
        "#...#...#..",
        ".#....#..#.",
        "..#.#...#.#",
        ".#...##..#.",
        "..#.##.....",
        ".#.#.#....#",
        ".#........#",
        "#.##...#...",
        "#...##....#",
        ".#..#...#.#"
    ]);

    let live : Vec<Vec<char>> = include_str!("day03.txt")
        .lines()
        .map(|x| x.chars().collect())
        .collect();

    let mut counts = Vec::<usize>::new();
    for (x,y) in vec![(1,1),(3,1),(5,1),(7,1),(1,2)] {
        counts.push( counttrees( &live, x, y ) );
    }

    println!("Part 1: {}", counts[1] );
    println!("Part 2: {}", counts.iter().fold(1, |tot,i| tot * i ) );
}
