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
    ".......S.......\n"
    "...............\n"
    ".......^.......\n"
    "...............\n"
    "......^.^......\n"
    "...............\n"
    ".....^.^.^.....\n"
    "...............\n"
    "....^.^...^....\n"
    "...............\n"
    "...^.^...^.^...\n"
    "...............\n"
    "..^...^.....^..\n"
    "...............\n"
    ".^.^.^.^.^...^.\n"
    "..............."
);

#define DAY "day07"

bool DEBUG = false;
bool TEST = false;


tuple<int,int64_t> part1 (StringVector data)
{
    int count = 0;
    map<int,int64_t> beams;
    for( auto & row : data )
    {
        auto i = row.find('S');
        if( i != row.npos )
        {
            beams[i] = 1;
            continue;
        }
        map<int,int64_t> nbeams;
        for( auto [i,c] : beams )
        {
            if( row[i] == '.' )
                nbeams[i] += c;
            else
            {
                count++;
                if( i > 0 )
                    nbeams[i-1] += c;
                if( i < row.size() - 1 )
                    nbeams[i+1] += c;
            }
        }

        beams.swap(nbeams);
    }
    int64_t sum = accumulate( 
        beams.begin(), 
        beams.end(), 
        0LL, 
        [](int64_t a, pair<int,int64_t> p){return a+p.second;}
    );
	return make_tuple( count, sum );
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
    StringVector lines = split(input);

    auto [p1,p2] = part1(lines);
    cout << "Part 1: " << p1 << "\n";
    cout << "Part 2: " << p2 << "\n";
}
