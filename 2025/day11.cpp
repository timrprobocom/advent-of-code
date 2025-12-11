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
    "aaa: you hhh\n"
    "you: bbb ccc\n"
    "bbb: ddd eee\n"
    "ccc: ddd eee fff\n"
    "ddd: ggg\n"
    "eee: out\n"
    "fff: out\n"
    "ggg: out\n"
    "hhh: ccc fff iii\n"
    "iii: out"
);

const string test2(
    "svr: aaa bbb\n"
    "aaa: fft\n"
    "fft: ccc\n"
    "bbb: tty\n"
    "tty: ccc\n"
    "ccc: ddd eee\n"
    "ddd: hub\n"
    "hub: fff\n"
    "eee: dac\n"
    "dac: fff\n"
    "fff: ggg hhh\n"
    "ggg: out\n"
    "hhh: out"
);

#define DAY "day11"

bool DEBUG = false;
bool TEST = false;

typedef map<string,list<string>> network_t;

network_t parse(StringVector & data )
{
    network_t connx;
    for( auto & line : data )
    {
        auto parts = split_list(line, " ");
        string name = parts.front();
        name = name.substr(0, name.size()-1);
        parts.pop_front();
        connx[name] = parts;
    }
	return connx;
}

map<string,int64_t> cache;

int64_t paths( network_t & connx, const string & start, const string & end )
{
    auto pr = cache.find(start+end);
    if( pr != cache.end() )
        return pr->second;

    int64_t sum = 0;
    if( find(connx[start].begin(), connx[start].end(), end) != connx[start].end() )
        sum = 1;

    for( auto n : connx[start] )
        sum += paths( connx, n, end );

	cache[start+end] = sum;
	return sum;
}


int64_t part1 ( StringVector & data )
{
    network_t connx = parse(data);
    return paths(connx, "you", "out");
}

int64_t part2 ( StringVector & data )
{
    network_t connx = parse(data);
    return paths(connx, "svr", "fft") * paths(connx, "fft", "dac") * paths(connx, "dac", "out") +
           paths(connx, "svr", "dac") * paths(connx, "dac", "fft") * paths(connx, "fft", "out");
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
    auto data = split(input);

    cout << "Part 1: " << part1(data) << "\n";
    cache.clear();
    if( TEST )
        data = split(test2);
    cout << "Part 2: " << part2(data) << "\n";
}
