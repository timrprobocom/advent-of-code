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

#if 0
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

tuple<double,double> find_mbx(int64_t x0, int64_t y0, int dx, int dy)
{
    double m = double(dy)/double(dx);
    double b = y0 - m * x0;
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
        dt[2] *= sign;
    }

    Point( const Point & pt )
        : pos(3)
        , dt(3)
    {
        copy( &pt.pos[0], &pt.pos[3], &pos[0] );
        copy( &pt.dt[0], &pt.dt[3], &dt[0] );
    }

    tuple<double,double> find_mbx() 
    { 
        return ::find_mbx(pos[0],pos[1],dt[0],dt[1]);
    }

    tuple<int64_t,int64_t,int64_t> at(int64_t t) 
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


tuple<int64_t,int64_t> intersect2d(double p1m, double p1b, double p2m, double p2b)
{
    // Are the lines parallel?
    if( p1m == p2m )
        return make_tuple(0,0);
    int64_t x = (p2b-p1b)/(p1m-p2m)+0.5;
    int64_t y = p1m*x+p1b+0.5;
    return make_tuple(x,y);
}

bool in_the_future(Point & pt1, int64_t x, int64_t y)
{
    // Did this happen in the future?
    return (pt1.dt[0] < 0) == (x < pt1.pos[0]);
}


int64_t part1( PointVector & vectors )
{
    int64_t rmin = TEST ?  7 : 200000000000000;
    int64_t rmax = TEST ? 28 : 400000000000000;
    int count = 0;
    for( int i = 0; i < vectors.size(); i++ )
    {
        auto [p1m,p1b] = vectors[i].find_mbx();
        for( int j = i+1; j < vectors.size(); j++ )
        {
            auto [p2m,p2b] = vectors[j].find_mbx();
            auto [x,y] = intersect2d(p1m,p1b,p2m,p2b);

            if( x && y && 
                in_the_future(vectors[i],x,y) && 
                in_the_future(vectors[j],x,y) &&
                (rmin <= x && x <= rmax && rmin <= y && y <= rmax)
            )
            {
                count++;
            }
        }
    }
    return count;
}

void subtract(LongVector & a, LongVector & b )
{
    a[0] -= b[0];
    a[1] -= b[1];
    a[2] -= b[2];
}

void crossproduct( LongVector & out, LongVector & a, LongVector & b )
{
    out.resize(a.size());
    out[0] = a[1]*b[2] - a[2]*b[1];
    out[1] = a[2]*b[0] - a[0]*b[2];
    out[2] = a[0]*b[1] - a[1]*b[0];
}

int64_t dotproduct( LongVector & a, IntVector & b )
{
    return a[0]*b[0] + a[1]*b[1] + a[2]*b[2];
}

// Find the velocity of the rock.

int find_rock_vel(PointVector & vectors, LongVector & result)
{
    // Create a system of equations.  Remember that we need this in Fortran
    // column-major order.

    vector<double> sys(9);
    vector<double> equals;

    for( int i = 0; i < 3; i++ )
    {
        Point & p1 = vectors[i];
        Point & p2 = vectors[(i+1)%3];

        LongVector pa(3);
        LongVector pb(3);


        pa[0] = p1.pos[0] - p2.pos[0];
        pa[1] = p1.pos[1] - p2.pos[1];
        pa[2] = p1.pos[2] - p2.pos[2];
        pb[0] = p1.dt[0] - p2.dt[0];
        pb[1] = p1.dt[1] - p2.dt[1];
        pb[2] = p1.dt[2] - p2.dt[2];

        LongVector dp;
        crossproduct( dp, pa, pb );
        sys[i+0] = dp[0];
        sys[i+3] = dp[1];
        sys[i+6] = dp[2];
        equals.push_back( dotproduct( dp, p2.dt ));
    }

    // Set up the call to LAPACK dgesv.

    int N = 3;
    int NRHS = 1;
    int LDA = 3;
    int IPIV[3];
    int LDB = 3;
    int info;

    dgesv_( &N, &NRHS, sys.data(), &LDA, IPIV, equals.data(), &LDB, &info );

    result.resize(3);
    result[0] = equals[0];
    result[1] = equals[1];
    result[2] = equals[2];

    return info;
}


// Given the velocity of the rock, find the initial position.

tuple<int64_t,int64_t,int64_t> find_rock_pos(PointVector & vectors, LongVector & drock)
{
    Point p1(vectors[0]);
    Point p2(vectors[1]);
    for( int i = 0; i < 3; i++ )
    {
        p1.dt[i] -= drock[i];
        p2.dt[i] -= drock[i];
    }

    auto [p1m,p1b] = find_mbx(p1.pos[0],p1.pos[1],p1.dt[0],p1.dt[1]);
    auto [p2m,p2b] = find_mbx(p2.pos[0],p2.pos[1],p2.dt[0],p2.dt[1]);

    // So, hailstones 0 and 1 intersect in x, y here:
    auto [x,y] = intersect2d(p1m,p1b,p2m,p2b);

    // At these times:
    int64_t ta = (x - p1.pos[0]) / p1.dt[0];
    int64_t tb = (x - p2.pos[0]) / p2.dt[0];

    // And what is that location in 3D?
    return p1.at(ta);
}


int64_t part2( PointVector & vectors )
{
    LongVector drock;
    find_rock_vel(vectors, drock);
    auto [x,y,z] = find_rock_pos(vectors, drock);
    return x+y+z;
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
    cout << "Part 2: " << part2(vectors) << "\n"; // 6654
}
