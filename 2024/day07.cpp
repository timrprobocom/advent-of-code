#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cstdint>
#include <cstring>
#include <vector>
#include <map>
#include <set>
#include <queue>
#include <algorithm>
#include <numeric>

using namespace std;

const string test(
"190: 10 19\n"
"3267: 81 40 27\n"
"83: 17 5\n"
"156: 15 6\n"
"7290: 6 8 6 15\n"
"161011: 16 10 13\n"
"192: 17 8 14\n"
"21037: 9 7 18 13\n"
"292: 11 6 16 20"
);

bool DEBUG = false;
bool TEST = false;

typedef vector<string> StringVector;

StringVector split( string src, string delim )
{
    StringVector sv;
    for( int j = src.find(delim); j != -1; )
    {
        sv.push_back( src.substr(0,j) );
        src = src.substr(j+delim.size());
        j = src.find(delim);
    }
    sv.push_back(src);
    return sv;
}


typedef vector<int64_t> LongVector;
typedef vector<LongVector>  LongBlock;
typedef set<int64_t>  LongSet;

int64_t part1(const LongBlock & data )
{
    int64_t sumx = 0;
    for( auto && row : data )
    {
        int64_t k = -1;
        LongSet maybe;
        for( int64_t v1 : row )
        {
            if( k < 0 )
                k = v1;
            else if( maybe.empty() )
                maybe.insert( v1 );
            else
            {
                LongSet next;
                for( auto m : maybe )
                {
                    next.insert(m+v1);
                    if( m*v1 <= k )
                        next.insert(m*v1);
                }
                maybe.swap( next );
            }
        }
        if( maybe.find( k ) != maybe.end() )
            sumx += k;
    }
    return sumx;
}

int64_t part2(const LongBlock & data )
{
    int64_t sumx = 0;
    for( auto && row : data )
    {
        int64_t k = -1;
        LongSet maybe;
        for( int64_t v1 : row )
        {
            if( k < 0 )
                k = v1;
            else if( maybe.empty() )
                maybe.insert( v1 );
            else
            {
                LongSet next;
                for( auto m : maybe )
                {
                    next.insert(m+v1);
                    int64_t p =  m*v1;
                    if( p <= k )
                        next.insert( p );
                    p = stoll(to_string(m)+to_string(v1));
                    if( p <= k )
                        next.insert( p );
                }
                maybe.swap( next );
            }
        }
        if( maybe.find( k ) !=  maybe.end() )
            sumx += k;
    }
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

    stringstream buffer;
    if( TEST )
    {
        buffer.str( test );
    }
    else 
    {
        buffer << ifstream("day07.txt").rdbuf();
    }

    LongBlock data;
    string word;
    while( buffer >> word )
    {
        if( word.back() == ':' )
        {
            word.pop_back();
            data.push_back(LongVector());
        }
        data.back().push_back( stoll(word));
    }

    cout << "Part 1: " << part1(data) << "\n";
    cout << "Part 2: " << part2(data) << "\n";
}