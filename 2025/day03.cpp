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
    "987654321111111\n"
    "811111111111119\n"
    "234234234234278\n"
    "818181911112111"
);

#define DAY "day03"

bool DEBUG = false;
bool TEST = false;

int64_t part2 (StringVector & data, int n)
{
	int64_t count = 0;
    for( auto & row : data )
    {
		// In each loop, we take the largest number that still leave enough room.

        string poss;
		int ix = 0;
        while( poss.size() < n )
        {
            int px = n - poss.size();
            auto m = max_element( &row[ix], &row[row.size() - px + 1]);
            poss = poss + *m;
            ix = (m - &row[0]) + 1;
		}

		count += stoll(poss);
		if( DEBUG )
            cout << row << " " << poss << "\n";
	}
	return count;
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
    StringVector data = split(input);
    
    cout << "Part 1: " << part2(data,2) << "\n";
    cout << "Part 2: " << part2(data,12) << "\n";
}
