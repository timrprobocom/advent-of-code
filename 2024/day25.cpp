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
"#####\n"
".####\n"
".####\n"
".####\n"
".#.#.\n"
".#...\n"
".....\n"
"\n"
"#####\n"
"##.##\n"
".#.##\n"
"...##\n"
"...#.\n"
"...#.\n"
".....\n"
"\n"
".....\n"
"#....\n"
"#....\n"
"#...#\n"
"#.#.#\n"
"#.###\n"
"#####\n"
"\n"
".....\n"
".....\n"
"#.#..\n"
"###..\n"
"###.#\n"
"###.#\n"
"#####\n"
"\n"
".....\n"
".....\n"
".....\n"
"#....\n"
"#.#..\n"
"#.#.#\n"
"#####"
);


bool DEBUG = false;
bool TEST = false;


// Any #/# invalidates.

int part1( vector<unsigned int> & locks, vector<unsigned int> & keys )
{
    int sumx = 0;
    for( auto l : locks )
        for( auto k : keys )
            if( !(l&k) )
                sumx++;
   return sumx;
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

    string input = TEST ? test : file_contents("day25.txt");

    // Convert to binary.

    vector<unsigned int> locks;
    vector<unsigned int> keys;
    unsigned int row;
    char last = '\n';
    for( auto c : input )
    {
        if( c == '#' )
            row = (row << 1) | 1;
        else if( c == '.' )
            row = (row << 1);
        else if( c == '\n' && last == '\n')
        {
            if( row & 1 )
                locks.push_back( row );
            else
                keys.push_back( row );
            row = 0;
        }
        last = c;
    }
    if( row & 1 )
        locks.push_back( row );
    else
        keys.push_back( row );

    cout << "Part 1: " << dec << part1(locks,keys) << "\n";
}
