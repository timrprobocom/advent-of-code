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
    "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}\n"
    "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}\n"
    "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"
);

#define DAY "day10"

bool DEBUG = false;
bool TEST = false;
bool TIMING = false;


#define _in_
#define _out_

void parse(
    _in_  StringVector & data,
    _out_ StringVector & lights,
    _out_ vector<vector<vector<int>>> & presses,
    _out_ IntMatrix & joltage
)
{
    lights.clear();
    presses.clear();
    joltage.clear();

    for( auto & line : data )
    {
        cout << "Parsing " << line << "\n";
        auto parts = split(line, " ");

        // This isn't right.  We need to how LARGE the lights array is.

        auto pf = parts.front();
        lights.push_back(pf.substr(1, pf.size()-2) );

        auto pb = parts.back().substr(1, parts.back().size()-2);
        joltage.push_back( split_int(pb,",") );

        IntMatrix pp;
        for( int i = 1; i < parts.size()-1; i++ )
        {
            auto pb = parts[i].substr(1, parts[i].size()-2);
            pp.push_back( split_int(pb, ",") );
        }
        presses.push_back( pp );
	}
}


string toggle(string lights, const IntVector & switches) 
{
    for( auto i : switches )
    {
        if( lights[i] == '#' )
            lights[i] = '.';
        else
            lights[i] = '#';
    }
    return lights;
}

int64_t part1 ( StringVector & lights, vector<vector<vector<int>>> & presses )
{
    int sum = 0;
    for( int i = 0; i < lights.size(); i++ )
    {
        string target = lights[i];
        IntMatrix & prs = presses[i];
        int found = 0;
        int bits = target.size();

        deque<tuple<int,int>> queue;
        for( int j = 0; j < prs.size(); j++ )
            queue.push_back( make_tuple(1<<j,1) );

        while( !queue.empty() )
        {
            auto [curr, count] = queue.front();
            queue.pop_front();

            // Try this combination.

            string mylights(bits, '.');
            for( int j = 0; j < bits; j++ )
                if( (curr>>j) & 1 )
                    mylights = toggle( mylights, prs[j] );

            if( mylights == target )
            {
                sum += count; // I need to know how many transformations have been make.
                break;
            }

            for( int j = 0; j < prs.size(); j++ )
                if( (1 << j) > curr )
                    queue.push_back( make_tuple(curr | (1 << j), count+1) );
		}
	}
	return sum;
}

int64_t part2 ( vector<vector<vector<int>>> presses, IntMatrix & joltage )
{
    return 0;
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

    StringVector lights;
    vector<vector<vector<int>>> presses;
    IntMatrix joltage;

    parse( lines, lights, presses, joltage );
    
    cout << "Part 1: " << part1(lights, presses) << "\n";
    cout << "Part 2: " << part2(presses, joltage) << "\n";
}
