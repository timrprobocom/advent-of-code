#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <cmath>
#include <vector>
#include <tuple>
#include <set>
#include <algorithm>

#ifndef M_PI
#define M_PI 3.14159265358979
#endif

// 3,4 with 8

const char * t1 = "\
.#..#\n\
.....\n\
#####\n\
....#\n\
...##\n\
";

// 5,6 with 33

const char * t2 = "\
#..#.#....\n\
..#######.\n\
.#.#.###..\n\
.#..#.....\n\
..#....#.#\n\
#..#....#.\n\
.##.#..###\n\
##...#..#.\n\
.#....####\n\
";


// 1,2 with 35

const char * t3 = "\
#.#...#.#.\n\
.###....#.\n\
.#....#...\n\
##.#.#.#.#\n\
....#.#.#.\n\
.##..###.#\n\
..#...##..\n\
..##....##\n\
......#...\n\
.####.###.\n\
";

// 6,3 with 41

const char * t4 = "\
.#..#..###\n\
####.###.#\n\
....###.#.\n\
..###.##.#\n\
##.##.#.#.\n\
....###..#\n\
..#.#..#.#\n\
#..#.#.###\n\
.##...##.#\n\
.....#.#..\n\
";

// 11,13 with 210

const char * t5 = "\
.#..##.###...#######\n\
##.############..##.\n\
.#.######.########.#\n\
.###.#######.####.#.\n\
#####.##.#.##.###.##\n\
..#####..#.#########\n\
####################\n\
#.####....###.#.#.##\n\
##.#################\n\
#####.##.###..####..\n\
..######..##.#######\n\
####.##.####...##..#\n\
.#####..#.######.###\n\
##...#.##########...\n\
#.##########.#######\n\
.####.#.###.###.#.##\n\
....##.##.###..#####\n\
.#.#.###########.###\n\
#.#.#.#####.####.###\n\
###.##.####.##.#..##\n\
";


struct Point {
    int x;
    int y;
    Point( )
        : x(0)
        , y(0)
        {}
    Point( int _x, int _y )
        : x(_x)
        , y(_y)
        {}

    bool operator< (const Point & other) const
    {
        return x < other.x || y < other.y;
    }

    bool operator== (const Point & other) const
    {
        return x==other.x && y==other.y;
    }

    bool operator!= (const Point & other) const
    {
        return x!=other.x || y!=other.y;
    }

    Point operator+( const Point & other )
    {
        return Point( x+other.x, y+other.y );
    }

    Point& operator+=( const Point & other )
    {
        x += other.x;
        y += other.y;
        return *this;
    }
};


//typedef std::vector<std::vector<char>> spacemap_t;

struct spacemap_t : public std::vector<std::vector<char>> 
{
    // This seems silly.

    std::vector<char> & operator[]( int y )
    {
        return at(y);
    }
    const std::vector<char> & operator[]( int y ) const
    {
        return at(y);
    }
    char & operator[]( const Point & pt )
    {
        return at(pt.y)[pt.x];
    }
    char operator[]( const Point & pt ) const
    {
        return at(pt.y)[pt.x];
    }
};


spacemap_t read( std::istream  && t )
{
    spacemap_t map;
    for( std::string ln; getline( t, ln); )
    {
        map.emplace_back( ln.size() );
        std::copy( 
            ln.begin(),
            ln.end(),
            map.back().begin()
        );
    }
    return map;
}


spacemap_t read( const char * t )
{
    return read( std::istringstream(t) );
}


int gcd( int x, int y )
{
    while( y )
    {
        int t = y;
        y = x % y;
        x = t;
    }
    return x;
}


bool visible( const spacemap_t & graph, Point p0, Point p1 )
{
    // Get the slope of the line.

    int dx = p1.x - p0.x;
    int dy = p1.y - p0.y;
    
    // Compute the GCD.  If they are relatively prime, then this star 
    // is visible.

    int div = gcd(abs(dx),abs(dy));
    if( div == 1 )
        return true;

    // Compute the steps at which stars will interfere.

    Point step( dx / div, dy / div );

    // Until we reach the target (which we always will), check for blocks.

    for( p0 += step; p0 != p1; p0 += step )
        if( graph[p0] == '#' )
            return false;

    return true;
}


std::set<Point> check( const spacemap_t & graph, Point(target) )
{
//    std::cout << "Checking " << target.x << " " <<  target.y << "\n";
    int dim = graph.size();
    std::set<Point> found;
    for( int y1=0; y1 < dim; y1++ )
    {
        for( int x1=0; x1 < dim; x1++ )
        {
            Point pt(x1,y1);
            if( pt == target )
                continue;
            if( graph[pt] != '#' )
                continue;
            if( visible( graph, target, pt ) )
            {
//                std::cout << "   " << pt.x << "," << pt.y << " visible\n";
                found.insert( pt );
            }
        }
    }
    return found;
}



std::pair<int,Point> scan(const spacemap_t & graph) 
{
    int maxcount = 0;
    Point maxelem(0,0);
    for( int y = 0; y < graph.size(); y++ )
    {
        auto ln = graph[y];
        for( int x = 0; x < ln.size(); x++ )
        {
            char cell = ln[x];
//            print( x, y, ln, cell )
            if( cell == '.' )
                continue;
            int count = check( graph, Point(x, y) ).size();
            if( count > maxcount )
            {
                maxcount = count;
                maxelem = Point(x,y);
            }
        }
    }
    std::cout << maxelem.x << "," << maxelem.y << " sees " << maxcount << "\n";
    return std::make_pair( maxcount, maxelem );
}


double angle( Point & a, Point & b )
{
    return M_PI/4 - atan2((a.x-b.x),(a.y-b.y));
}


int laser(spacemap_t graph, Point target)
{
    int remains = 200;
    std::set<Point> found;

    // If we don't catch them all in one round, eliminate this whole set.

    while( (found = check(graph,target)).size() < remains )
    {
        for( auto pt : found )
            graph[pt] = '.';
        remains -= found.size();
    }

    // Convert to a vector.

    std::vector<Point> data;
    data.resize( found.size() );
    std::copy( found.begin(), found.end(), data.begin() );

    std::sort(
        data.begin(),
        data.end(),
        [&target](Point & a, Point & b) {
            return angle(a,target) < angle(b,target);
        } 
    );

    std::cout << "Number 200 is " 
        << data[remains-1].x << ","
        << data[remains-1].y << "\n";

    return data[remains-1].x * 100 + data[remains-1].y;
}


void part1()
{
    scan(read(t1));
    scan(read(t2));
    scan(read(t3));
    scan(read(t4));
    scan(read(t5));
    std::cout 
        << "\nPart 1: " 
        << scan(read(std::ifstream("day10.txt"))).first << "\n";
}

// Answer was 26, 29.
        
void part2()
{
    Point best = scan(read(t5)).second;
    std::cout << laser( read(t5), best ) << "\n";

    // Find the point with the most visible asteroids.
    best = scan(read(std::ifstream("day10.txt"))).second;

    // Find the 200th blasted asteroid.
    std::cout 
        << "\nPart 2: " 
        << laser(read(std::ifstream("day10.txt")), best)  << "\n";
}

int main()
{
    part1();
    std::cout << std::endl;
    part2();
}
