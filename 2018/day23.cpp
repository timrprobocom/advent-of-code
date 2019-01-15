#include <fstream>
#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <iterator>


struct Bot
{
    int x;
    int y;
    int z;
    int r;

    Bot( int _x, int _y, int _z, int _r=0 )
        : x( _x ) , y( _y ) , z( _z ) , r( _r )
    {}

    void multiply( int scale )
    {
        x *= scale;
        y *= scale;
        z *= scale;
        r *= scale;
    }

    Bot add( int dx, int dy, int dz, int dr=0 ) const
    {
        return Bot( x+dx, y+dy, z+dz, r+dr );
    }

    Bot divide( int scale ) const
    {
        int half = scale/2;
        return Bot( 
            (x+half)/scale,
            (y+half)/scale,
            (z+half)/scale,
            (r+half)/scale
        );
    }
};

typedef std::vector<Bot> botlist_t;

Bot scan( botlist_t & bots )
{
    bots.clear();
    int maxr = 0;
    Bot maxbot(0,0,0,0);
    while( std::cin )
    {
        std::string line;
        std::getline( std::cin, line );
        if( line.empty() )
            break;
        
        int i1 = line.find( '<' );
        int i2 = line.find( ',' );
        int i3 = line.find( ',', i2+1 );
        int i4 = line.find( '>' );
        int i5 = line.find( "r=" );

        int x = std::stoi(line.substr( i1+1, i2-i1 ));
        int y = std::stoi(line.substr( i2+1, i3-i2 ));
        int z = std::stoi(line.substr( i3+1, i4-i3 ));
        int r = std::stoi(line.substr( i5+2 ));

        bots.emplace_back( x, y, z, r );

        if( r > maxr )
        {
            maxr = r;
            maxbot = bots.back();
        }
    }
    return maxbot;
}


int mandist( Bot a, Bot b )
{
    return std::abs(a.x-b.x)+std::abs(a.y-b.y)+std::abs(a.z-b.z);
}

bool inRange( Bot b, Bot pt )
{
    return mandist( b, pt ) <= b.r;
}

int Part1( botlist_t & bots, Bot maxbot )
{
    return
        std::count_if( 
            bots.begin(), bots.end(), 
            [&maxbot](Bot bot){ return inRange(maxbot,bot); }
        );
}


Bot Part2( int DIVISOR, botlist_t & bots, int scale, Bot centroid )
{
    int bound = DIVISOR * 3 / 2;
    botlist_t subbots;
    std::transform(
        bots.begin(), bots.end(),
        std::back_inserter(subbots),
        [scale](Bot base) { return base.divide(scale); }
    );
std::cout << "Centroid: (" << centroid.x << "," << centroid.y << "," << centroid.z << ")\n";
    

    Bot maxloc(0,0,0,0);
    int maxcnt = 0;
    for( int z = -bound; z < bound; z++ )
        for( int y = -bound; y < bound; y++ )
            for( int x = -bound; x < bound; x++ )
            {
                Bot check = centroid.add(x, y, z);
                int cnt = std::count_if(
                    subbots.begin(), subbots.end(),
                    [&check] (Bot bot) { return inRange( bot, check ); }
                );
                if( cnt > maxcnt )
                {
                    maxcnt = cnt;
                    maxloc = check;
                    std::cout 
                        << maxcnt << " @ ("
                        << maxloc.x << ","
                        << maxloc.y << ","
                        << maxloc.z << ")\n";
                }
            }
    return maxloc;
}

int less_than_100m( int factor )
{
    int base = 1;
    while( base < 99999999 )
        base *= factor;
    return base;
}


int main( int argc, char ** argv )
{
    int DIVISOR = 10;
    if( argc > 1 )
        DIVISOR = std::stoi( *++argv );

    botlist_t bots;
    Bot maxbot = scan(bots);
    std::cout << "Max r:" << maxbot.r << "\n";
    std::cout << "Part 1:" << Part1(bots, maxbot) << "\n";

    int base = less_than_100m( DIVISOR );
    Bot centroid(0,0,0,0);
    for( int scale = base; scale > 0; scale /= DIVISOR )
    {
        std::cout << "Checking scale " << scale << "\n";
        centroid.multiply( DIVISOR );
        centroid = Part2( DIVISOR, bots, scale, centroid );
    }

    Bot zero(0,0,0,0);
    std::cout << "Part 2: " << mandist(centroid,zero) << "\n";
}
