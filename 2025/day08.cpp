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
#include <chrono>

#include "utils.h"

using namespace std;

const string test(
    "162,817,812\n"
    "57,618,57\n"
    "906,360,560\n"
    "592,479,940\n"
    "352,342,300\n"
    "466,668,158\n"
    "542,29,236\n"
    "431,825,988\n"
    "739,650,466\n"
    "52,470,668\n"
    "216,146,977\n"
    "819,987,18\n"
    "117,168,530\n"
    "805,96,715\n"
    "346,949,466\n"
    "970,615,88\n"
    "941,993,340\n"
    "862,61,35\n"
    "984,92,344\n"
    "425,690,689"
);

#define DAY "day08"

bool DEBUG = false;
bool TEST = false;
bool TIMING = false;

struct Point3d {
    int64_t x;
    int64_t y;
    int64_t z;
};

int64_t dist3d(Point3d & a, Point3d & b) 
{
    return  (b.x-a.x)*(b.x-a.x) + 
            (b.y-a.y)*(b.y-a.y) + 
            (b.z-a.z)*(b.z-a.z);
}

struct Dist {
    int64_t dist;
    int64_t a;  // hash
    int64_t b;  // hash
};

inline int64_t hashx( const Point3d & pt )
{
    return (pt.x << 18) | pt.y;
}

inline void getCounts( map<int,int> & counts, const map<int64_t,int> & circuits )
{
    counts.clear();
    for( auto ct : circuits )
        counts[ct.second] ++;
}

int64_t part1 ( const vector<Point3d> & data, const vector<Dist> & dists )
{
    // We assign each junction to a circuit.

    map<int64_t,int> circuit;
    for( int i = 0; i < data.size(); i++ )
        circuit[hashx(data[i])] = i;

    const int limit = TEST ? 10 : 1000;
    for( int i = 0; i < limit; i++ )
    {
        int bindex = circuit[dists[i].b];
        for( auto & ct : circuit )
            if( ct.second == bindex )
                circuit[ct.first] = circuit[dists[i].a];
    }

    // Find the 3 most common.
    
    map<int,int> counts;
    getCounts(counts, circuit);
    vector<int> countx;
    for( auto & c : counts )
        countx.push_back( c.second );
    sort( countx.begin(), countx.end(), [](int a, int b){return b<a;} );
    if( DEBUG )
        for( auto pt : countx )
            cout << pt << "\n";

    return countx[0] * countx[1] * countx[2];
}

int64_t part2 ( const vector<Point3d> & data, const vector<Dist> & dists )
{
    // We assign each junction to a circuit.

    map<int64_t,int> circuit;
    for( int i = 0; i < data.size(); i++ )
        circuit[hashx(data[i])] = i;

    map<int,int> counts;
    for( auto & dist : dists )
    {
        int bindex = circuit[dist.b];
        for( auto & ct : circuit )
            if( ct.second == bindex )
                circuit[ct.first] = circuit[dist.a];

        getCounts(counts, circuit);
        if( counts.size() == 1 )
            return (dist.a >> 18) * (dist.b >> 18);
    }

    return 0;
}

int main( int argc, char ** argv )
{
    auto start = chrono::system_clock::now();
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

    // Construct points.
    
    vector<Point3d> points;
    points.reserve( lines.size() );
    for( auto & line : lines )
    {
        auto p = split(line,",");
        points.emplace_back(Point3d{
            stoll(p[0]),
            stoll(p[1]),
            stoll(p[2])
        });
    }

    vector<int64_t> hashes;
    hashes.reserve( points.size() );
    for( auto & pt : points )
        hashes.push_back( hashx(pt) );

    // Construct the distances.

    vector<Dist> distances;
    distances.reserve( points.size() );
    for( int i = 0; i < points.size(); i++ )
        for( int j = i+1; j < points.size(); j++ )
            distances.emplace_back(Dist{
                dist3d(points[i], points[j]),
                hashes[i],
                hashes[j]
            });

    sort( 
        distances.begin(),
        distances.end(),
        [](Dist & a, Dist & b){ return a.dist < b.dist; } 
    );
    if( DEBUG )
        for( auto & d : distances )
            printf( "%15ld %15ld %15ld\n", d.dist, d.a, d.b );

    auto p1 = chrono::system_clock::now();
    cout << "Part 1: " << part1(points, distances) << "\n";
    auto p2 = chrono::system_clock::now();
    cout << "Part 2: " << part2(points, distances) << "\n";
    auto p3 = chrono::system_clock::now();

    if( TIMING )
    {
        auto part1 = p2-p1;
        auto part2 = p3-p2;
        auto full = p3-start;

        cout << "\n";
        cout << "Part 1: " << chrono::duration_cast<chrono::milliseconds>(part1).count() << "ms\n";
        cout << "Part 2: " << chrono::duration_cast<chrono::milliseconds>(part2).count() << "ms\n";
        cout << "All:    " << chrono::duration_cast<chrono::milliseconds>(full).count() << "ms\n";
    }
}
