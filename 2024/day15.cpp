#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <iterator>
#include <cmath>
#include <cstdint>
#include <cstring>
#include <vector>
#include <map>
#include <algorithm>
#include <numeric>

#include "utils.h"

using namespace std;

const string test(
"##########\n"
"#..O..O.O#\n"
"#......O.#\n"
"#.OO..O.O#\n"
"#..O@..O.#\n"
"#O#..O...#\n"
"#O..O..O.#\n"
"#.OO.O.OO#\n"
"#....O...#\n"
"##########\n"
"\n"
"<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^\n"
"vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v\n"
"><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<\n"
"<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^\n"
"^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><\n"
"^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^\n"
">^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^\n"
"<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>\n"
"^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>\n"
"v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^\n"
);

const string test2(
"########\n"
"#..O.O.#\n"
"##@.O..#\n"
"#...O..#\n"
"#.#.O..#\n"
"#...O..#\n"
"#......#\n"
"########\n"
"\n"
"<^^>>>vv<v>>v<<\n"
);

bool DEBUG = false;
bool TEST = false;
#define DAY "day15"

int WIDTH = -1;
int HEIGHT = -1;

typedef Point<short> point_t;

inline point_t dirs(char c)
{
    switch( c )
    {
        case '<': return point_t(-1, 0);
        case '^': return point_t(0, -1);
        case '>': return point_t(1, 0);
        case 'v': return point_t(0,1);
    }
    return point_t(0,0);
}


void printgrid(vector<vector<char>> & grid)
{
    for( auto & row : grid )
        cout << string(row.begin(), row.end()) << "\n";
    cout << endl;
}




// We call ourselves recursively, because when moving vertically,
// the number of cells being affected can double:
//  ...[][]...
//  ....[]....
//  .....@....

bool can_we_move(vector<vector<char>> & grid, point_t pt, point_t delta )
{
    vector<point_t> affected;
    affected.push_back( pt );

    char c = grid[pt.y][pt.x];
    if( delta.y )
    {
        if( c == '[' )
            affected.push_back( pt + dirs('>') );
        else if ( c == ']' )
            affected.push_back( pt + dirs('<') );
    }

    for( auto & pt : affected )
    {
        point_t npt = pt + delta;
        char dc = grid[npt.y][npt.x];
        if( dc == '.' )
            continue;
        else if( dc == '#' )
            return false;
        else if( dc == 'O' || dc == '[' || dc == ']' )
            if( ! can_we_move(grid, npt, delta) )
                return false;
    }
    return true;
}

bool do_a_move(vector<vector<char>> & grid, point_t pt, point_t delta )
{
    if( !can_we_move(grid, pt, delta) )
        return false;

    vector<point_t> affected;
    affected.push_back( pt );

    char c = grid[pt.y][pt.x];
    if( delta.y )
    {
        if( c == '[' )
            affected.push_back( pt + dirs('>') );
        else if ( c == ']' )
            affected.push_back( pt + dirs('<') );
    }
    
    for( auto & pt : affected )
    {
        char c = grid[pt.y][pt.x];
        point_t npt = pt+delta;
        char dc = grid[npt.y][npt.x];
        if( dc == '#' )
        {
            cout << "Assertion 1 failed\n";
            printgrid(grid);
            cout << pt.x << "," << pt.y << " " << npt.x << "," << npt.y << "\n";
            return false;
        }
        else if( dc == '.' )
        {
            grid[pt.y][pt.x] = '.';
            grid[npt.y][npt.x] = c;
        }
        else if( dc == 'O' || dc == '[' || dc == ']' )
        {
            do_a_move(grid, npt, delta);
            grid[pt.y][pt.x] = '.';
            grid[npt.y][npt.x] = c;
        }
    }
    return true;
}


int64_t part1(vector<vector<char>> grid, point_t robot, string & moves )
{
    if( DEBUG )
    {
        cout << "START\n";
        printgrid(grid);
    }

    for( char c : moves )
    {
        if( do_a_move(grid, robot, dirs(c)) )
            robot += dirs(c);
    }
    if( DEBUG )
        printgrid(grid);

    int score = 0;
    for( int y = 0; y < grid.size(); y++ )
        for( int x = 0; x < grid[y].size(); x++ )
            if( grid[y][x] == 'O' || grid[y][x] == '[' )
                score += y * 100 + x;
    return score;
}


int main( int argc, char ** argv )
{
    while( *++argv )
    {
        string arg(*argv);
        if( arg == "debug")
            DEBUG = true;
        else if( arg =="test")
            TEST = true;
    }

    string input = TEST ? test : file_contents(DAY".txt");

    vector<vector<char>> sgrid;
    vector<vector<char>> dgrid;
    point_t srobot;
    point_t drobot;
    string moves;

    for( auto & line : split(input) )
    {
        if( line.empty() )
            continue;
        if( line[0] == '#' )
        {
            vector<char> drow;
            int y = sgrid.size();
            sgrid.push_back( vector<char>(line.begin(), line.end()));
            for( int x = 0; x < line.size(); x++ )
            {
                char c = line[x];
                if( c == 'O' )
                {
                    drow.push_back( '[' );
                    drow.push_back( ']' );
                }
                else if( c == '@' )
                {
                    drow.push_back( '@' );
                    drow.push_back( '.' );
                    srobot = point_t(x,y);
                    drobot = point_t(x+x,y);
                } 
                else
                {
                    drow.push_back( c );
                    drow.push_back( c );
                }
            }
            dgrid.push_back( drow );
        }
        else
            moves += line;
    }
 
    if( DEBUG )
    {
        cout << "srobot: " << srobot.x << "," << srobot.y << "\n";
        cout << "drobot: " << drobot.x << "," << drobot.y << "\n";
    }
 
    cout << "Part 1: " << part1(sgrid, srobot, moves) << "\n";
    cout << "Part 2: " << part1(dgrid, drobot, moves) << "\n";
}

