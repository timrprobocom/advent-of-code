#include <fstream>
#include <iostream>
#include <list>
#include <algorithm>

bool DEBUG = false;
bool TEST = false;

int part1( int data )
{
    std::list<int> buffer;
    buffer.push_back( 0 );
    int rounds = 2017;
    std::list<int>::iterator posn = buffer.begin();

    for( int i = 1; i <= rounds; i++ )
    {
        for( int m = 0; m < data+1; m++ )
        {
            if( posn == buffer.end() )
                posn = buffer.begin();
            posn++;
        }
        posn = buffer.insert( posn, i );
    }

    auto p = std::find( buffer.begin(), buffer.end(), 2017 );

    if( DEBUG )
        std::cout << *p << ", ";
    p++;
    if( DEBUG )
        std::cout << *p << "\n";

    return *p;
}

int part2( int data )
{
    int rounds = 5000000;
    int size = 1;
    int pos = 0;
    int result = 0;

    for( int i = 0; i < rounds; i++ )
    {
        int newx = (pos + data) % size + 1;
        if( newx == 1 )
            result = i+1;

        pos = newx;
        size ++;
    }
    return result;
}

int main( int argc, char ** argv )
{
    std::string name = *argv;
    while( *++argv )
    {
        std::string arg(*argv);
        if( arg == "debug")
            DEBUG = true;
        else if( arg =="test")
            TEST = true;
    }

    int data = TEST ? 3 : 328;

    std::cout << "Part 1: " << part1(data) << "\n";
    std::cout << "Part 2: " << part2(data) << "\n";
}

