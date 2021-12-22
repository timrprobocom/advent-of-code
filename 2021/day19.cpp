#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <set>
#include <map>

using namespace std;

#include "utils.h"

typedef vector<Point> PointList;
typedef set<Point> PointSet;
typedef map<int,int> Rotations;
typedef map<int,Point> Offsets;
typedef vector<PointList> ScannerSet;

bool DEBUG = false;

struct Information {
    PointSet beacons;
    Rotations rotations;
    Offsets offsets;
};


void read( 
    istream && ifs,
    ScannerSet & scanners
)
{
    scanners.clear();
    for( string line; getline(ifs, line); )
    {
        if( line.size() < 2 )
            continue;
        if( line.substr(0,3) == "---"  )
            scanners.resize( scanners.size() + 1 );
        else
        {
            char c;
            int i, j, k;
            istringstream fin( line );
            fin >> i >> c >> j >> c >> k;
            scanners.back().emplace_back( i, j, k );
        }
    }
}




// This returns a vector of the 24 possible rotations of this point.
// Move the "facing" direction through all 6 points, then rotate around
// that axis four times.

void allrotate( PointList & out, const Point in )
{
    Point pt = in;
    out.clear();

    for( int i = 0; i < 2; i++ )
        for( const char * axis = "xxxzyyyxzzzy"; *axis; axis++ )
        {
            out.push_back( pt );
            pt.rotate(*axis);
        }
}


// This function answers the musical question, for each pair of points
// in the two scan lists, if they lined up, how many other points would
// line up?

bool find_matches( PointList scan1, PointList scan2, Point & delta )
{
    PointSet set1( scan1.begin(), scan1.end() );
    for( auto && pt1 : scan1 )
        for( auto && pt2 : scan2 )
        {
            int matches = 0;
            delta = pt2 - pt1;
            for( auto && pt2x : scan2 )
                if( set1.find( pt2x - delta ) != set1.end() )
                    matches += 1;
            if( matches >= 12 )
                return true;
        }
    return false;
}


bool process( ScannerSet scanners, /*out*/ Information & info )
{
    // Make all rotations of all scanner readings.
    // This is a 25x24 array.
    // rotations[i][j] is the set of points for scanner i in rotation j.

    vector< vector< PointList > > rotations;

    rotations.resize( scanners.size() );
    for( auto && r : rotations )
        r.resize( 24 );
    
    PointList rots;
    for( int i = 0; i < scanners.size(); i++ )
    {
        for( auto && pt : scanners[i] )
        {
            allrotate( rots, pt );
            for( int j = 0; j < rots.size(); j++ )
                rotations[i][j].push_back( rots[j] );
        }
    }

    PointSet & beacons = info.beacons;
    Rotations & known_r = info.rotations;
    Offsets & known_o = info.offsets;

    // This is the set of known beacons.

    beacons = PointSet( rotations[0][0].begin(), rotations[0][0].end() );
    known_r[0] = 0;
    known_o[0] = Point(0,0,0);

    while( known_r.size() < rotations.size() )
    {
        for( int i = 0; i < rotations.size(); i++ )
        {
            if( known_r.find(i) != known_r.end() )
                continue;

            vector<PointList> & scan1 = rotations[i];

            bool escape = false;

            // scan1 is the candidate scanner we want to place.

            for( auto && rot2 : known_r )
            {
                int j = rot2.first;
                auto & pt2 = known_o[j];
                auto & scan2 = rotations[j][rot2.second];

                // scan2 is a scanner whose position and rotation is now known.

                for( int possrot = 0; possrot < 24; possrot++ )
                {
                    // Does this rotation of scan1 line up with scan2?

                    Point potential;
                    if( !find_matches( scan2, scan1[possrot], potential ) )
                        continue;

                    if( DEBUG )
                    {
                        cout << "Matched " <<  i << "  rot " << possrot << " vs " << j << "\n";
                    }

                    // We have a winner.  Add this to the set of knowns.
                    // We shift scan1 to match the coords of scan2, then
                    // shift that to our master coords.

                    for( auto && pt : scan1[possrot] )
                    {
                        beacons.insert( (pt - potential) - pt2 );
                    }

                    known_r[i] = possrot;
                    known_o[i] = potential + pt2;
                    escape = true;
                    break;
                }

                if( escape )
                    break;
            }
        }
    }

    return true;
}

int part1( const Information & info )
{
    return info.beacons.size();
}

int part2( const Information & info )
{
    int maxx = 0;
    for( auto && pt1 : info.offsets )
        for( auto && pt2 : info.offsets )
        {
            int dist = pt1.second.mandist( pt2.second );
            if( dist > maxx )
                maxx = dist;
        }
    return maxx;
}

int main( int argc, char ** argv )
{
    const char * filename = "day19.txt";
    while( *++argv )
    {
        if( strcmp(*argv, "debug") == 0 )
            DEBUG = true;
        else if( strcmp(*argv, "test") == 0 )
            filename = "test19.txt";
    }

    vector<PointList> scanners;
    read( ifstream(filename), scanners );

    Information info;
    process(scanners, info);

    cout << "Part 1: " << part1(info) << "\n";
    cout << "Part 2: " << part2(info) << "\n";
    return 0;
}
