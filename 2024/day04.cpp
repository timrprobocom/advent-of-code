#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <iterator>
#include <cstdint>
#include <cstring>
#include <cmath>
#include <vector>
#include <algorithm>
#include <numeric>

#include "utils.h"

using namespace std;

const string test(
"MMMSXXMASM\n"
"MSAMXMSMSA\n"
"AMXSXMAAMM\n"
"MSAMASMSMX\n"
"XMASAMXAMM\n"
"XXAMMXXAMA\n"
"SMSMSASXSS\n"
"SAXAMASAAA\n"
"MAMMMXMMMM\n"
"MXMXAXMASX"
);

bool DEBUG = false;
bool TEST = false;
#define DAY "day04"

int WIDTH = -1;
int HEIGHT = -1;
typedef Point<short> point_t;

point_t dirs[] = {
    point_t(-1,-1), point_t(-1,0), point_t(-1,1),
    point_t( 0,-1),                point_t( 0,1),
    point_t( 1,-1), point_t( 1,0), point_t( 1,1)
};

// Find all occurrances of c.

vector<point_t> findall( const StringVector & grid, char c )
{
    vector<point_t> result;
    for( int y=0; y < HEIGHT; y++ )
        for( int x=0; x < WIDTH; x++ )
            if( grid[y][x] == c )
                result.push_back( point_t(x,y) );
    return result;
}

int part1( StringVector & data )
{
    int winner = 0;
    string search("MAS");
    for( auto & xy : findall(data, 'X') )
    {
        for( auto & dxy : dirs )
        {
            int x = xy.x;
            int y = xy.y;
            winner++;
            for( auto c : search )
            {
                x += dxy.x;
                y += dxy.y;
                if( x < 0 || x >= WIDTH || y < 0 || y >= HEIGHT || data[y][x] != c)
                {
                    winner--;
                    break;
                }
            }
        }
    }
    return winner;
}

int part2( StringVector & data )
{
    int winner = 0;
    for( auto & xy : findall(data, 'A') )
    {
        winner += 
            0 < xy.x && xy.x < WIDTH-1 && 0 < xy.y && xy.y < HEIGHT-1 &&
            (
                (data[xy.y-1][xy.x-1] == 'M' && data[xy.y+1][xy.x+1] == 'S') ||
                (data[xy.y-1][xy.x-1] == 'S' && data[xy.y+1][xy.x+1] == 'M')
            )
            &&
            (
                (data[xy.y+1][xy.x-1] == 'M' && data[xy.y-1][xy.x+1] == 'S') ||
                (data[xy.y+1][xy.x-1] == 'S' && data[xy.y-1][xy.x+1] == 'M')
            );
    };
    return winner;
}

int main( int argc, char ** argv )
{
    string name = *argv;
    while( *++argv )
    {
        string arg(*argv);
        if( arg == "debug")
            DEBUG = true;
        else if( arg =="test")
            TEST = true;
    }

    string input = TEST ? test : file_contents(DAY".txt");
    StringVector grid = split(input);
    WIDTH = grid[0].size();
    HEIGHT = grid.size();

    cout << "Part 1: " << part1(grid) << "\n";
    cout << "Part 2: " << part2(grid) << "\n";
}
