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
    "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"
);

#define DAY "day02"

bool DEBUG = false;
bool TEST = false;

int64_t part1 (string  data)
{
    int64_t count = 0;
    for( auto & row : split(data,",")) 
    {
        auto rg = split(row,"-");
        string l = rg[0];
        string r = rg[1];
        int64_t ln = stoll(l);
        int64_t rn = stoll(r);

        // If they are not the same length, adjust the odd one.
		// If left is odd, replace it by 1000.
		// If right is odd, replace it by 9999.

        if( l.size() % 2 )
            if( r.size() % 2 )
                continue;
            else {
                l = "1" + l;
                fill( l.begin()+1, l.end(), '0');
            }
        else if( r.size() % 2 )
        {
            r.resize(l.size());    
            fill( r.begin(), r.end(), '9' );
        }

		// We can now assert that both numbers have an even number of digits.

		string lhalf = l.substr(0, l.size()/2);
		int64_t lhalfn = stoll(lhalf);
		int64_t rhalfn = stoll(r.substr(0, l.size()/2)) + 1;

		while( lhalfn < rhalfn )
        {
            int64_t llln = stoll( to_string(lhalfn) + to_string(lhalfn) );
			if( ln <= llln && llln <= rn )
				count += llln;
			lhalfn++;
		}
		if( DEBUG )
			cout << l << " " << r << " " << count << "\n";
    }
    return count;
}

// This is a shameful brute force approach.

bool check(int64_t num)
{
    string ns = to_string(num);
    int n = ns.size();
	for( int i = 1; i <= n/2; i++ )
    {
		if( n % i )
			continue;

		bool ok = true;
        for( int j = i; j < n; j += i )
        {
            if(ns.substr(j,i) != ns.substr(0,i) )
            {
                ok = false;
                break;
			}
		}
		if( ok ) {
			return true;
		}
	}
	return false;
}

int64_t part2 (string data)
{
    int64_t count = 0;
    for( auto & row : split(data,",")) 
    {
        auto rg = split(row,"-");
        string l = rg[0];
        string r = rg[1];
        int64_t ln = stoll(l);
        int64_t rn = stoll(r);

        for( int64_t n = ln; n < rn; n++ )
            if( check(n) )
                count += n;

        if (DEBUG) 
			cout << l << " " << r << " " << count << "\n";
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
    
    cout << "Part 1: " << part1(input) << "\n";
    cout << "Part 2: " << part2(input) << "\n";
}
