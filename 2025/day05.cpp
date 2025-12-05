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
    "3-5\n"
    "10-14\n"
    "16-20\n"
    "12-18\n"
    "\n"
    "1\n"
    "5\n"
    "8\n"
    "11\n"
    "17\n"
    "32"
);

#define DAY "day05"

bool DEBUG = false;
bool TEST = false;

struct Range {
    int64_t lo;
    int64_t hi;
};

typedef vector<Range> RangeVector;

int part1( RangeVector ranges, vector<int64_t> codes )
{
    int count = 0;
    for( auto c : codes )
        for( auto & r : ranges )
            if( r.lo <= c && c <= r.hi )
            {
                count++;
                break;
            }
    return count;
}

int64_t part2 (RangeVector ranges )
{
    sort( ranges.begin(), ranges.end(), [](Range & a, Range & b) {return a.lo < b.lo;});
    int64_t total = 0;
    int64_t high = 0;
    for( auto & r : ranges )
    {
        if( DEBUG )
            cout << high << " " << r.lo << " " << r.hi << "\n";

        if( high < r.lo )
        {
            total += r.hi - r.lo + 1;
            high = r.hi + 1;
        }
        else if( high <= r.hi )
        {
            total += r.hi - high + 1;
            high = r.hi + 1;
        }
    }
	return total;
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
    RangeVector ranges;
    vector<int64_t> codes;
    for( auto row : lines )
    {
        if( row.empty() )
            continue;
        auto i = row.find('-');
        if( i == row.npos )
            codes.push_back( stoll(row) );
        else {
            ranges.emplace_back( Range({
                stoll( row.substr(0,i)),
                stoll( row.substr(i+1))
            }));
        }
    }
    
    cout << "Part 1: " << part1(ranges,codes) << "\n";
    cout << "Part 2: " << part2(ranges) << "\n";
}
