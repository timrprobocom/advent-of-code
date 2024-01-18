#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cstring>
#include <vector>
#include <map>
#include <set>
#include <queue>
#include <algorithm>
#include <numeric>

using namespace std;

#define IN
#define OUT
#define INOUT

#if 0
// We use LAPACK's for singles, dgesv_ for doubles.
//
// sgesv_ is a symbol in the LAPACK library files for solving systems 
// of linear equations.  Note that the inputs must be column-major.

extern "C" int dgesv_(
     IN  int * N,     // number of equations (3)
     IN  int * NRHS,  // number of right-hand sides (1)
   INOUT double * A,
     IN  int * LDA,   // leading dimension of A
     OUT int * IPIV,        // pivot indexes 
   INOUT double * B,
     IN  int * LDB,
     OUT int * info     // success/fail code, 0=OK
 );

// Holy crap, this works.

int main()
{
    int N = 3;
    int NRHS = 1;
    double A[] = { -16, 0, -12, -8, -8, 2, -4, 4, -3 };
    int LDA = 3;
    int IPIV[3];
    double B[] = { 32, 0, 32 };
    int LDB = 3;
    int info;

    sgesv_( &N, &NRHS, A, &LDA, IPIV, B, &LDB, &info );
    std::cout << "info = " << info << "\n";
    std::cout << "B = " << B[0] << ", " << B[1] <<", " << B[2] << "\n";
}
#endif

bool DEBUG = false;
bool TEST = false;

typedef vector<string> StringVector;
typedef vector<int> IntVector;
typedef vector<int64_t> LongVector;
typedef vector<vector<uint8_t>> ByteGrid;

const string test(
"19, 13, 30 @ -2,  1, -2\n"
"18, 19, 22 @ -1, -1, -2\n"
"20, 25, 34 @ -2, -2, -4\n"
"12, 31, 28 @ -1, -2, -1\n"
"20, 19, 15 @  1, -5, -3"
);

tuple<double,int64_t> find_mbx(int64_t x0, int64_t y0, int dx, int dy)
{
    double m = double(dy)/double(dx);
    int64_t b = y0 - m * x0;
    return make_tuple(m,b);
}

struct Point
{
    vector<int64_t> pos;
    vector<int> dt;

    Point( int64_t x0, int64_t y0, int64_t z0, int dx0, int dy0, int dz0 )
    {
        pos.push_back( x0 );
        pos.push_back( y0 );
        pos.push_back( z0 );
        dt.push_back( dx0 );
        dt.push_back( dy0 );
        dt.push_back( dz0 );
    }

    Point( string row )
        : pos(3)
        , dt(3)
    {
        int i = 0;
        int sign = 1;

        for( char c : row )
        {
            if( isdigit(c) )
            {
                if( i < 3 )
                    pos[i] = pos[i] * 10 + c - '0';
                else
                    dt[i-3] = dt[i-3] * 10 + c - '0';
            }
            else if( c == '-' )
                sign = -1;
            else if( c != ' ' )
            {
                if( i < 3 )
                    pos[i] *= sign;
                else
                    dt[i-3] *= sign;
                i += 1;
                sign = 1;
            }
        }
    }

    Point( const Point & pt )
        : pos(3)
        , dt(3)
    {
        copy( &pt.pos[0], &pt.pos[3], &pos[0] );
        copy( &pt.dt[0], &pt.dt[3], &dt[0] );
    }

    tuple<double,int64_t> find_mbx() 
    { 
        return ::find_mbx(pos[0],pos[1],dt[0],dt[1]);
    }

    tuple<int64_t,int64_t,int64_t> at(int t) 
    {
        int64_t p0 = pos[0] + t * dt[0];
        int64_t p1 = pos[1] + t * dt[1];
        int64_t p2 = pos[2] + t * dt[2];
        return make_tuple(p0,p1,p2);
    }
};

typedef vector<Point> PointVector; 

void parse( string & data, PointVector & points ) {
    istringstream parse(data);
    string line;
    while( getline( parse, line ) )
        points.emplace_back(line);
}


tuple<int64_t,int64_t> intersect2d(double p1m, int64_t p1b, double p2m, int64_t p2b)
{
    // Are the lines parallel?
    if( p1m == p2m )
        return make_tuple(0,0);
    int64_t x = (p2b-p1b)/(p1m-p2m)+0.5;
    int64_t y = p1m*x+p1b+0.5;
    return make_tuple(x,y);
}

bool in_the_future(Point & pt1, Point & pt2, int x, int y)
{
    // Did this happen in the future?
    return ((pt1.dt[0] < 0) == (x < pt1.pos[0])) && ((pt2.dt[0] < 0) == (x < pt2.pos[0]));
}


int64_t part1( PointVector & vectors )
{
    int64_t rmin = TEST ?  7 : 200000000000000;
    int64_t rmax = TEST ? 28 : 400000000000000;
    cout << rmin << " " << rmax << "\n";
    int count = 0;
    for( int i = 0; i < vectors.size(); i++ )
    {
        auto [p1m,p1b] = vectors[i].find_mbx();
        for( int j = i+1; j < vectors.size(); j++ )
        {
            auto [p2m,p2b] = vectors[j].find_mbx();
            auto [x,y] = intersect2d(p1m,p1b,p2m,p2b);
            if( x && y && in_the_future(vectors[i],vectors[j],x,y) )
            {
                if( (rmin <= x && x <= rmax && rmin <= y && y <= rmax) )
                    cout << x << " " << y << ": " 
                        << p1m << " " << p1b << " " 
                        << p2m << " " << p2b << ": " 
                        << vectors[i].pos[1] << " " << vectors[j].pos[1] << "\n";
                count += (rmin <= x && x <= rmax && rmin <= y && y <= rmax);
            }
        }
    }
    return count;
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

    string data;
    if( TEST )
    {
        data = test;
    }
    else 
    {
        stringstream buffer;
        buffer << ifstream("day24.txt").rdbuf();
        data = buffer.str();
    }


    PointVector vectors;
    parse( data, vectors );

    cout << "Part 1: " << part1(vectors) << "\n"; // 2154
//    cout << "Part 2: " << part2(vectors) << "\n"; // 6654
}



#if 0
# Find the velocity of the rock.

def find_rock_vel(vectors):
    p1 = vectors[0]
    p2 = vectors[1]
    p3 = vectors[2]
    sys = np.array([
        np.cross(p1.pos-p2.pos,p1.dt-p2.dt),
        np.cross(p2.pos-p3.pos,p2.dt-p3.dt),
        np.cross(p3.pos-p1.pos,p3.dt-p1.dt)
    ])
    if DEBUG:
        print(sys)
    equals = np.array([
        np.dot(sys[0],p2.dt),
        np.dot(sys[1],p3.dt),
        np.dot(sys[2],p1.dt)
    ])
    return np.linalg.solve(np.array(sys), equals).round().astype(int)

# Given the velocity of the rock, find the initial position.

def find_rock_pos(vectors, drock):
    p1 = vectors[0].copy()
    p2 = vectors[1].copy()
    p1.dt = p1.dt - drock
    p2.dt = p2.dt - drock

    p1m,p1b = find_mbx(p1.pos[0],p1.pos[1],p1.dt[0],p1.dt[1])
    p2m,p2b = find_mbx(p2.pos[0],p2.pos[1],p2.dt[0],p2.dt[1])

    # So, hailstones 0 and 1 intersect in x, y here:
    x,y = intersect2d(p1m,p1b,p2m,p2b)

    # At these times:
    ta = int((x - p1.pos[0]) / p1.dt[0])
    tb = int((x - p2.pos[0]) / p2.dt[0])

    # And what is that location in 3D?
    return p1.at(ta)

def part2(vectors):
    drock = find_rock_vel(vectors)
    prock = find_rock_pos(vectors, drock)
    return sum(prock)
#endif
