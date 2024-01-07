#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cstring>
#include <array>
#include <vector>
#include <set>
#include <algorithm>
#include <numeric>

using namespace std;

bool DEBUG = false;
bool TEST = false;

const string test(
"Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53\n"
"Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19\n"
"Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1\n"
"Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83\n"
"Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36\n"
"Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11\n"
);

typedef vector<string> StringVector;
typedef vector<int> IntVector;

int score( IntVector & wins, IntVector & mine )
{
    sort( wins.begin(), wins.end() );
    sort( mine.begin(), mine.end() );
    IntVector sect;
    set_intersection( 
        wins.begin(), wins.end(), 
        mine.begin(), mine.end(),
        back_inserter(sect)
    );
    return sect.size();
}

void parse( istream & fin, vector<IntVector> & left, vector<IntVector> & right )
{
    string word;
    bool leftside = true;
    IntVector leftset;
    IntVector rightset;
    while( fin >> word )
    {
        if( word.back() == ':' )
        {
            leftside = true;
        }
        else if( word == "|" )
        {
            leftside = false;
        }
        else if( word == "Card" )
        {
            if( !leftset.empty() )
            {
                left.push_back( leftset );
                right.push_back( rightset );
            }
            leftset.clear();
            rightset.clear();
        }
        else
        {
            int val = stol(word);
            if( leftside )
                leftset.push_back( val );
            else
                rightset.push_back( val );
        }
    }
    if( !leftset.empty() )
    {
        left.push_back( leftset );
        right.push_back( rightset );
    }
}

int part1( vector<IntVector> & left, vector<IntVector> & right )
{
    int sumx = 0;
    for( int i = 0; i < left.size(); i++ )
    {
        int cnt = score(left[i], right[i]);
        if( cnt )
            sumx += 1 << (cnt-1);
    }
    return sumx;
}


int part2( vector<IntVector> & left, vector<IntVector> & right )
{
    IntVector copies(200, 1);
    int sumx = 0;
    for( int i = 0; i < left.size(); i++ )
    {
        sumx += copies[i];
        int cnt = score(left[i], right[i]);
        for( int j = 0; j < cnt; j++ )
            copies[i+j+1] += copies[i];
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

    istringstream data;
    if( TEST )
    {
        data.str( test );
    }
    else 
    {
        stringstream buffer;
        buffer << ifstream("day04.txt").rdbuf();
        data.str( buffer.str() );
    }

    vector<IntVector> lefts;
    vector<IntVector> rights;
    parse( data, lefts, rights );

    cout << "Part 1: " << part1(lefts, rights) << "\n";
    cout << "Part 2: " << part2(lefts, rights) << "\n";
}
