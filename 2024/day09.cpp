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

#include "utils.h"

using namespace std;

const string test(
"2333133121414131402"
);

bool DEBUG = false;
bool TEST = false;

#define DAY "day09"

template <typename T>
void qprint( deque<T> & q )
{
    for( auto d : q )
        cout << d << " ";
    cout << "\n";
}

int64_t part1( const vector<short> & data )
{
    deque<short> disk;

    for( int i=0; i < data.size(); i+=2 )
    {
        disk.resize( disk.size()+data[i  ], i/2 );
        disk.resize( disk.size()+data[i+1], -1 );
    }
    
    // Now compact it.

    int i = 0;
    int j = disk.size() - 1;

    while( i < j )
    {
        while( disk[i] >= 0 )
            i++;
        while( disk[j] < 0 )
            j--;
        if( i < j )
        {
            disk[i] = disk[j];
            disk[j] = -1;
            i++;
            j--;
        }
    }
    
    if( DEBUG )
        qprint(disk);

    // Evaluate.

    int64_t sumx = 0;
    for( int n=0; n < disk.size(); n++ )
        if( disk[n] >= 0 )
            sumx += n*disk[n];
    return sumx;
}


// Combine free blocks and remove empty ones.

void coalesce( deque<int> & space, int start, int size )
{
    deque<int> newspace;
    int i = 0;
    for( i = 0; i < space.size(); i += 2 )
    {
        int sstart = space[i];
        int ssize = space[i+1];

        if( !ssize )
            continue;

        else if( start > sstart+ssize )
        {
            newspace.push_back( sstart );
            newspace.push_back( ssize );
        }
        else if( start+size == sstart )
        {
            newspace.push_back( start );
            newspace.push_back( size+ssize );
            i += 2;
            break;
        }
        else if( sstart+ssize == start )
        {
            newspace.push_back( sstart );
            newspace.push_back( size+ssize );
            i += 2;
            break;
        }
        else if( sstart > start+size )
        {
            newspace.push_back( start );
            newspace.push_back( size );
            break;
        }
    }
    if( i < space.size() )
        copy( space.begin()+i, space.end(), back_inserter(newspace) );
    
    space.swap( newspace );
}

// Find the first hold large enough to hold this file.

int find_hole_below( const deque<int> & space, int start, int size )
{
    for( int i=0; i < space.size(); i+=2 )
    {
        if( space[i] > start )
            return -1;
        if( space[i+1] >= size )
            return i/2;
    }
    return -1;
}

int64_t part2( const vector<short> & data )
{
    int locate = 0;

    deque<int> files;
    deque<int> space;
    for( int i=0; i < data.size(); i+=2 )
    {
        files.push_back( locate );
        files.push_back( data[i] );
        locate += data[i];
        if( i < data.size() - 1 && data[i+1] )
        {
            space.push_back( locate );
            space.push_back( data[i+1] );
            locate += data[i+1];
        }
    }

    if( DEBUG )
    {
        cout << "files: ";
        qprint(files);
        cout << "space: ";
        qprint(space);
    }

    // Now try to move all the files starting from the end.

    for( int i=files.size()-2; i >= 0; i-=2 )
    {
        int start = files[i];
        int size = files[i+1];

        short n = find_hole_below( space, start, size );
        if( n >= 0 )
        {
            // Move this file.  Reduce empty space.
            files[i] = space[n*2+0];
            space[n*2+0] += size;
            space[n*2+1] -= size; 
            coalesce(space, start, size);
        }
    }
    
    if( DEBUG )
    {
        //files.sort();
        cout << "Final files: ";
        qprint(files);
        cout << "Final space: ";
        qprint(space);
    }

    int64_t sumx = 0;
    for( int i=0; i < files.size(); i+=2 )
    {
        int start = files[i];
        int size = files[i+1];
        int64_t idn = i/2;
        sumx += idn * (start * size + size * (size-1) / 2);
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

    string input = TEST ? test : file_contents(DAY".txt");
    if( input.back() == '\n' )
        input.pop_back();

    vector<short> disk;
    transform(
        input.begin(),
        input.end(),
        back_inserter(disk),
        [](char c) {return c-'0';}
    );

    cout << "Part 1: " << part1(disk) << "\n";
    cout << "Part 2: " << part2(disk) << "\n";
}
