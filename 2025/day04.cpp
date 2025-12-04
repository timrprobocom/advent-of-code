#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <iterator>
#include <cstdint>
#include <cstring>
#include <cmath>
#include <vector>
#include <map>
#include <set>
#include <queue>
#include <algorithm>
#include <numeric>

#include "utils.h"

using namespace std;

const string test(
    "..@@.@@@@.\n"
    "@@@.@.@.@@\n"
    "@@@@@.@.@@\n"
    "@.@@@@..@.\n"
    "@@.@@@@.@@\n"
    ".@@@@@@@.@\n"
    ".@.@.@.@@@\n"
    "@.@@@.@@@@\n"
    ".@@@@@@@@.\n"
    "@.@.@@@.@."
);

#define DAY "day04"

bool DEBUG = false;
bool TEST = false;

typedef Point<int> point_t;
point_t directions[] = {
    point_t(-1,-1), point_t(-1,0), point_t(-1,1),
    point_t( 0,-1),                point_t( 0,1),
    point_t( 1,-1), point_t( 1,0), point_t( 1,1)
    };

typedef set<point_t> pointset_t;

int neighbors1( const pointset_t & rolls, const point_t & pt )
{
    int count = 0;
    for( auto & dxy : directions )
    {
        count += rolls.find(pt+dxy) != rolls.end();            
    }
    return count;
}

int neighbors( const pointset_t & rolls, const point_t & pt )
{
    return count_if(
        begin(directions), end(directions),
        [&rolls,pt](point_t & dxy) {
            return rolls.find(pt+dxy) != rolls.end();
        }
    );
}

int part1( const pointset_t & rolls )
{
    int total = 0;
    for( auto && pt : rolls )
        total += neighbors(rolls, pt) < 4;
    return total;
}

int part2 (pointset_t & rolls )
{
    int removed = 0;
	for( ;; )
    {
		pointset_t nrolls;
        copy_if(
            rolls.begin(),
            rolls.end(),
            inserter(nrolls, nrolls.begin()),
            [&rolls](const point_t & pt) { return neighbors(rolls, pt) >= 4; }
        );
        if( rolls.size() == nrolls.size() )
            break;
		removed += rolls.size() - nrolls.size();
		rolls = nrolls;
	}
	return removed;
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
    pointset_t data;
    for( int y = 0; y < grid.size(); y++ )
        for( int x = 0; x < grid[y].size(); x++ )
            if( grid[y][x] == '@' )
                data.insert( point_t(x,y) );
    
    cout << "Part 1: " << part1(data) << "\n";
    cout << "Part 2: " << part2(data) << "\n";
}
