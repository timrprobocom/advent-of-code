#include <fstream>
#include <iostream>
#include <string>
#include <array>
#include <vector>
#include <algorithm>
#include "utils.h"

using namespace std;

typedef vector<string> Grid;

bool DEBUG = false;

std::array<Point,8> deltas { 
    Point(-1,-1),Point(-1,0),Point(-1,1),
    Point( 0,-1),            Point( 0,1),
    Point( 1,-1),Point( 1,0),Point( 1,1)
};

int countOccupied( Grid & grid )
{
    int count = 0;
    for( auto line : grid )
        for( char c : line )
            if( c == '#' )
                count++;
    return count;
}

void printGrid( Grid & grid )
{
    for( auto & line : grid )
        cout << line << "\n";
}

Grid part1step( Grid & grid )
{
    int xlen = grid[0].size();
    int ylen = grid.size();
    Grid newGrid;
    for( int y = 0; y < ylen; y++ )
    {
        string newLine;
        for( int x = 0; x < xlen; x++ )
        {
            char c = grid[y][x];
            if( c == '.' )
            {
                newLine += c;
                continue;
            }

            int adjacent = count_if(
                deltas.begin(), deltas.end(),
                [&](Point dxy) {
                    return
                        ((x+dxy.x) >= 0) && ((x+dxy.x) < xlen) &&
                        ((y+dxy.y) >= 0) && ((y+dxy.y) < ylen) &&
                        grid[y+dxy.y][x+dxy.x] == '#';
                }
            );
                   
            if( c == 'L' && adjacent == 0 )
                newLine += '#';
            else if( c == '#' && adjacent >= 4 )
                newLine += 'L';
            else
                newLine += c;
        }
        newGrid.push_back( newLine );
    }
    return newGrid;
}

Grid part2step( Grid & grid )
{
    int xlen = grid[0].size();
    int ylen = grid.size();
    Grid newGrid;
    for( int y = 0; y < ylen; y++ )
    {
        string newLine;
        for( int x = 0; x < xlen; x++ )
        {
            char c = grid[y][x];
            if( c == '.' )
            {
                newLine += c;
                continue;
            }

            int adjacent = 0;
            for( auto & dxy : deltas )
            {
                for(
                    Point probe(x+dxy.x,y+dxy.y);
                    ((probe.x) >= 0) && ((probe.x) < xlen) &&
                    ((probe.y) >= 0) && ((probe.y) < ylen) &&
                    grid[probe.y][probe.x] != 'L';
                    probe += dxy
                )
                {
                    if( grid[probe.y][probe.x] == '#')
                    {
                        adjacent++;
                        break;
                    }
                }
            }

            if( c == 'L' && adjacent == 0 )
                newLine += '#';
            else if( c == '#' && adjacent >= 5 )
                newLine += 'L';
            else
                newLine += c;
        }
        newGrid.push_back( newLine );
    }
    return newGrid;
}

void read( Grid & grid, istream & ifs )
{
    for( string line; getline(ifs, line); )
        grid.push_back( line );
}

int main( int argc, char ** argv)
{
    const char * filename = "day11.txt";
    while( *++argv )
    {
        string arg(*argv);
        if( arg == "debug")
            DEBUG = true;
        else if( arg == "test")
            filename = "day11.test.txt";
    }

    Grid data;
    ifstream fin(filename);
    read( data, fin );

    // Part 1.

    Grid grid = data;
    for(;;) {
        if( DEBUG ) {
            cout << countOccupied( grid ) << "\n";
            printGrid( grid );
        }
        Grid grid2 = part1step(grid);
        if( grid == grid2 )
            break;
        grid = grid2;
    }

    cout << "Part 1: " << countOccupied( grid ) << "\n";

    // Part 2.

    grid = data;
    for(;;) {
        if( DEBUG ) {
            cout << countOccupied( grid ) << "\n";
            printGrid( grid );
        }
        Grid grid2 = part2step(grid);
        if( grid == grid2 )
            break;
        grid = grid2;
    }

    cout << "Part 2: " << countOccupied( grid ) << "\n";
}


