#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cstring>
#include <vector>
#include <set>
#include <algorithm>
#include <numeric>

using namespace std;

bool DEBUG = false;

const char * test1 = 
"Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green\n"
"Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue\n"
"Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red\n"
"Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red\n"
"Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green\n"
;

struct color {
    int game;
    int red;
    int green;
    int blue;
};

typedef vector<color> ColorVector;

void reformat( istringstream & data, ColorVector & records )
{
    string word;
    color track = { 0, 0, 0, 0 };
    int hold = 0;
    while( data >> word )
    {
        if( word.back() == ':' )
        {
            word.pop_back();
            track.game = stol(word);
            continue;
        }
        if( word == "Game" )
        {
            records.push_back( track );
            track.red = track.green = track.blue = 0;
            continue;
        }

        if( isdigit(word[0]) )
        {
            hold = stol(word);
            continue;
        }

        bool push = false;
        if( word.back() == ';' )
        {
            push = true;
            word.pop_back();
        }
        if( word.back() == ',' )
            word.pop_back();

        if( word == "red" )
            track.red += hold;
        else if( word == "blue" )
            track.blue += hold;
        else if( word == "green" )
            track.green += hold;
        if( push )
        {
            records.push_back( track );
            track.red = track.green = track.blue = 0;
        }
    }
    records.push_back( track );
}


int part1( ColorVector & clrs )
{
    int sum = 0;
    int game = -1;
    int skip = -1;
    for( auto & c : clrs )
    {
        if( c.game != game )
        {
            sum += c.game;
            game = c.game;
        }
        if( c.game != skip )
        {
            if( c.red > 12 || c.green > 13 || c.blue > 14 )
            {
                sum -= c.game;
                skip = c.game;
            }
        }
    }
    return sum;
}

int part2( ColorVector & clrs )
{
    int sum = 0;
    int game = -1;
    color maxx = { 0, 0, 0 };
    for( auto & c : clrs )
    {
        if( c.game != game )
        {
            sum += maxx.red * maxx.green * maxx.blue;
            maxx.red = maxx.green = maxx.blue = 0;
            game = c.game;
        }
        maxx.red = max( maxx.red, c.red );
        maxx.green = max( maxx.green, c.green );
        maxx.blue = max( maxx.blue, c.blue );
    }
    sum += maxx.red * maxx.green * maxx.blue;
    return sum;
}

int main( int argc, char ** argv )
{
    istringstream data1;
    while( *++argv )
    {
        string arg(*argv);
        if( arg == "debug")
            DEBUG = true;
        else if( arg =="test")
        {
            data1.str( test1 );
        }
    }

    if( data1.str().empty() )
    {
        stringstream buffer;
        buffer << ifstream("day02.txt").rdbuf();
        data1.str( buffer.str() );
    }

    ColorVector clrs;
    reformat( data1, clrs );

    cout << "Part 1: " << part1(clrs) << "\n";
    cout << "Part 2: " << part2(clrs) << "\n";
}

