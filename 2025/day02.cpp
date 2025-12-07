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

int64_t check1( string lo, string hi )
{
    int ln = lo.size();
	int64_t lov = stoll(lo);
	int64_t hiv = stoll(hi);
	set<int64_t> found;

	for( int i = 1; i < ln; i++ )
    {
		if( ln%i )
			continue;

		int64_t s = stoll(lo.substr(0,i));
		int64_t e = stoll(hi.substr(0,i));
        for( int64_t p = s; p <= e; p++ )
        {
            string pp = to_string(p);
            string pp1;
            for( int j = 0; j < ln/i; j++ )
                pp1 += pp;
            int64_t st = stoll( pp1 );
			if( lov <= st && st <= hiv ) {
				found.insert(st);
			}
		}
	}
	return accumulate( found.begin(), found.end(), 0LL );
}

int64_t check(string lo, string hi)
{
    int ln = lo.size();
    int hn = hi.size();
    if( ln == hn )
        return check1(lo, hi);

    return check1(lo, string(ln,'9')) + check1( "1"+string(ln,'0'), hi); 
}

int64_t part2 (string data)
{
    int64_t count = 0;
    for( auto & row : split(data,",")) 
    {
        auto rg = split(row,"-");
        string l = rg[0];
        string r = rg[1];
        count += check(l, r);
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
