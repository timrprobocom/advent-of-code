#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <iterator>
#include <cstdint>
#include <limits.h>
#include <cstring>
#include <cmath>
#include <vector>
#include <map>
#include <set>
#include <queue>
#include <algorithm>
#include <numeric>

using namespace std;

const string test(
"1\n"
"10\n"
"100\n"
"2024"
);

const string test2(
"1\n"
"2\n"
"3\n"
"2024"
);

bool DEBUG = false;
bool TEST = false;

#define OUT
#define IN
   
// Sequence: x64, mix, prune?
// /32, mix, prune
// *2024, mix, prune
//
// Mix = bitwise xor
// Prune = mod 16777216

int gen(int secret)
{
    secret = (secret ^ (secret <<  6)) & 0xFFFFFF;
    secret = (secret ^ (secret >>  5)) & 0xFFFFFF;
    secret = (secret ^ (secret << 11)) & 0xFFFFFF;
    return secret;
}

int64_t part1(vector<int> data)
{
    int64_t sumx = 0;
    for( auto secret : data )
    {
        for( int i = 0; i < 2000; i++ )
            secret = gen(secret);
        sumx += secret;
    }
    return sumx;
}


// Generate the part2 prices and deltas from a given secret.

void sequence( OUT vector<int> & prices, OUT vector<int> & deltas, int secret )
{
    prices.clear();
    deltas.clear();
    prices.push_back( secret % 10 );
    deltas.push_back( 0 );

    for( int i=0; i < 2000; i++ )
    {
        int news = gen(secret);
        prices.push_back( news%10 );
        deltas.push_back( news%10 - secret%10 );
        secret = news;
    }
}


// Generate all of the 4-tuples from the deltas and the price at the end.

typedef int four_t;
four_t make4tuple( vector<int>::pointer begin, vector<int>::pointer end )
{
    four_t res = 0;
    for( ; begin != end; begin++ )
        res = res * 20 + *begin + 9;
    return res;
}

int64_t part2(vector<int> data)
{
    map<four_t, int64_t> fours;
    vector<int> prices;
    vector<int> deltas;
    for( auto secret : data )
    {
        sequence( prices, deltas, secret );
        set<four_t> seen;
        for( int i = 0; i < prices.size()-4; i++ )
        {
            four_t key = make4tuple(&deltas[i], &deltas[i+4]);
            if( seen.find(key) == seen.end() )
            {
                fours[key] += prices[i+3];
                seen.insert( key );
            }
        }
    }
    int64_t res = 0;
    for( auto kv : fours )
        res = max(res, kv.second);
    return res;
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

    stringstream input;
    if( TEST )
    {
        input << test;
    }
    else
    {
        input << ifstream("day22.txt").rdbuf();
    }

    vector<int> data{
        istream_iterator<int>(input),
        istream_iterator<int>()
    };

    cout << "Part 1: " << part1(data) << "\n";
    cout << "Part 2: " << part2(data) << "\n";
}
