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
"r, wr, b, g, bwu, rb, gb, br\n"
"\n"
"brwrr\n"
"bggr\n"
"gbbr\n"
"rrbgbr\n"
"ubwu\n"
"bwurrg\n"
"brgr\n"
"bbrgwb"
);


bool DEBUG = false;
bool TEST = false;
#define DAY "day19"

bool startswith( string & haystack, string needle )
{
    return haystack.substr(0, needle.size()) == needle;
}

int possible( vector<string> & towels, string & need, string sofar="")
{
    if( need == sofar )
        return 1;

    for( auto & t : towels )
        if( startswith(need, sofar+t) && possible(towels, need, sofar+t) )
            return 1;
    return 0;
}

// In both cases, the loop is slightly faster than the accumulate call.

int part1( vector<string> & towels, vector<string> & needs )
{
#if 0
    return accumulate(
        needs.begin(),
        needs.end(),
        0,
        [&towels](int sum, string n) {
            return sum + possible(towels, n);
        });
#else
    int sum = 0;
    for( auto & n : needs )
        sum += possible(towels, n);
    return sum;
#endif
}

map<string,int64_t> cache;
int64_t howmany( vector<string> & towels, string & need, string sofar="" )
{
    if( need == sofar )
        return 1;
    string key = need + "/" + sofar;
    if( cache.find(key) != cache.end() )
        return cache[key];
#if 0
    int64_t sum = accumulate(
        towels.begin(),
        towels.end(),
        0ll,
        [&towels, &need, &sofar] (int64_t sum, string t) {
            return startswith(need, sofar+t )
                ? sum+howmany(towels, need, sofar+t)
                : sum;
    });
#else
    int64_t sum = 0;
    for( auto & t : towels )
        if( startswith(need, sofar+t) )
            sum += howmany(towels, need, sofar+t);
#endif
    cache[key] = sum;
    return sum;
}

int64_t part2( vector<string> & towels, vector<string> & needs )
{
    int64_t sum = 0;
    for( auto & n : needs )
        sum += howmany(towels, n);
    return sum;
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

    string data = TEST ? test : file_contents(DAY".txt");

    vector<string> needs = split(data);
    vector<string> towels = split(needs.front(), ", ");
    needs.erase(needs.begin(), needs.begin()+2);

    cout << "Part 1: " << part1(towels, needs) << "\n";
    cout << "Part 2: " << part2(towels, needs) << "\n";
}
