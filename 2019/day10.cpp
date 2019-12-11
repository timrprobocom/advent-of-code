#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <cmath>
#include <vector>
#include <set>
#include <algorithm>
#define M_PI 3.14159265358979

// 3,4 with 8

const char * t1 = "\
.#..#\
.....\
#####\
....#\
...##\
";

// 5,6 with 33

const char * t2 = "\
#..#.#....\
..#######.\
.#.#.###..\
.#..#.....\
..#....#.#\
#..#....#.\
.##.#..###\
##...#..#.\
.#....####\
";


// 1,2 with 35

const char * t3 = "\
#.#...#.#.\
.###....#.\
.#....#...\
##.#.#.#.#\
....#.#.#.\
.##..###.#\
..#...##..\
..##....##\
......#...\
.####.###.\
";

// 6,3 with 41

const char * t4 = "\
.#..#..###\
####.###.#\
....###.#.\
..###.##.#\
##.##.#.#.\
....###..#\
..#.#..#.#\
#..#.#.###\
.##...##.#\
.....#.#..\
";

// 11,13 with 210

const char * t5 = "\
.#..##.###...#######\
##.############..##.\
.#.######.########.#\
.###.#######.####.#.\
#####.##.#.##.###.##\
..#####..#.#########\
####################\
#.####....###.#.#.##\
##.#################\
#####.##.###..####..\
..######..##.#######\
####.##.####...##..#\
.#####..#.######.###\
##...#.##########...\
#.##########.#######\
.####.#.###.###.#.##\
....##.##.###..#####\
.#.#.###########.###\
#.#.#.#####.####.###\
###.##.####.##.#..##\
";

typedef std::vector<std::vector<char>> spacemap_t;

spacemap_t read( const char * t )
{
    spacemap_t map;
    std::istringstream iss( t );
    for( std::string ln; getline( iss, ln); )
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

spacemap_t read( std::istream & t )
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

struct Point {
    int x;
    int y;
    Point( int _x, int _y )
        : x(_x)
        , y(_y)
        {}

    bool operator< (const Point & other) const
    {
        return (abs(x)+abs(y)) < (abs(other.x)+abs(other.y));
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


bool visible( spacemap_t & graph, Point p0, Point p1 )
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
    {
        if( graph[p0.y][p0.x] == '#' )
            return false;
    }
    return true;
}


std::set<Point> check( spacemap_t & graph, Point(target) )
{
//    std::cout << "Checking" << target.x << " " <<  target.y << "\n";
    int dim = graph.size();
    std::set<Point> found;
    for( int y1=0; y1 < dim; y1++ )
        for( int x1=0; x1 < dim; x1++ )
        {
            Point pt(x1,y1);
            if( pt == target )
                continue;
            if( graph[y1][x1] != '#' )
                continue;
            if( visible( graph, target, pt ) )
                found.insert( pt );
        }
//  std::cout << found.size() << "\n";
    return found;
}



int scan(spacemap_t graph) 
{
    int maxcount = 0;
    Point maxelem(0,0);
    for( int y = 0; y < graph.size(); y++ )
    {
        auto ln = graph[y];
        for( int x = 0; y < ln.size(); x++ )
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
    return maxcount; //, maxelem;
}



int laser(spacemap_t graph, Point target)
{
    int remains = 200;
    while( remains )
    {
        std::set<Point> found = check(graph,target);
// If we don't catch them all in one round, eliminate these.
        if( found.size() < remains )
        {
            for( auto pt : found )
                graph[pt.y][pt.x] = '.';
            remains -= found.size();
            continue;
        }
        break;

        auto angle = [&target](Point& pt) {
            return M_PI/4 - atan2((pt.x-target.x),(pt.y-target.y));
        };

        // Convert to a vector.

        std::vector<Point> data;
        data.resize( found.size() );
        std::copy( found.begin(), found.end(), data.begin() );

        std::sort(
            data.begin(),
            data.end(),
            [&target, angle](Point & a, Point & b) {
                return angle(a) < angle(b);
            } 
        );

        std::cout << "Number 200 is " 
            << data[remains-1].x << ","
            << data[remains-1].y << "\n";

        return data[remains-1].y * 100 + data[remains-1].x;
    }
    return 0;
}

    

void part1()
{
    scan(read(t1));
    scan(read(t2));
    scan(read(t3));
    scan(read(t4));
    scan(read(t5));
    std::cout << "Part 1: " << scan(read(std::ifstream("day10.txt")))[0] << "\n";
}

// Answer was 26, 29.
        
void part2()
{
    Point best = scan(read(t5))[1];
    laser( read(t5), best );
    best = scan(read(std::ifstream("day10.txt")))[1];
    std::cout << "\nPart 2: " << laser(read(std::ifstream("day10.txt")), best)  << "\n";
}

int main()
{
    part1();
    std::cout << std::endl;
    part2();
}
