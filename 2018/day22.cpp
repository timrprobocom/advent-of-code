#include <map>
#include <set>
#include <tuple>
#include <string>
#include <vector>
#include <fstream>
#include <iostream>
#include <algorithm>

bool gVerbose = false;
int gDepth = 0;
int gTargetX = 0;
int gTargetY = 0;

// Test data:   510  10 10
//    Answer: 116   45
// Tim's data: 3339 10 715
//    Answer: 7915  980
// Bog's data:   6969  9 796
//    Answer: 7901  1087

const int KY = 48271;
const int KX = 16807;
const int KMOD = 20183;
const int PAD = 30;

enum gear_t {NONE,TORCH,GEAR};

typedef std::tuple<int,int> Coord;
typedef std::tuple<int,int,int> CoordPlus;
typedef std::map<CoordPlus,int> CostMap;
typedef std::map<CoordPlus,CoordPlus> TrackMap;

CoordPlus make( Coord c, int tool )
{
    return CoordPlus(std::get<0>(c),std::get<1>(c),tool);
}

struct Cave
{
    int m_Depth;
    std::map< Coord, int > m_Erosion;

    Cave( int depth, Coord & target )
        : m_Depth( depth )
    {
        m_Erosion[Coord(0,0)] = gDepth;
        m_Erosion[target] = gDepth;
    }

    int gete( int x, int y )
    {
        Coord c(x,y);
        if( m_Erosion.find(c) != m_Erosion.end() )
            return m_Erosion[c];
        int e = 0;
        if( !x )
            e = (y * KY + m_Depth) % KMOD;
        else if( !y )
            e = (x * KX + m_Depth) % KMOD;
        else
            e = (gete(x-1,y) * gete(x,y-1) + m_Depth) % KMOD;
        m_Erosion[c] = e;
        return e;
    }

    int get(int x, int y )
    {
        return gete(x,y) % 3;
    }
};


void ShowPlot( TrackMap & backtrack, CoordPlus winner )
{
    // Find maxima.

    int maxx = 0;
    int maxy = 0;
    for( 
        CoordPlus node = winner;
        backtrack.find(node) != backtrack.end();
        node = backtrack[node]
    )
    {
        maxx = std::max( maxx, std::get<0>(node) );
        maxy = std::max( maxy, std::get<1>(node) );
    }

    std::cout << "Maxima: " << maxx << " " << maxy << "\n";

    // Plot it.

    std::vector<std::string> grid;
    grid.resize( maxy+1, std::string(maxx+1, ' '));
    grid[0][0] = '#';

    for( 
        CoordPlus node = winner;
        backtrack.find(node) != backtrack.end();
        node = backtrack[node]
    )
    {
        grid[std::get<1>(node)][std::get<0>(node)] = '#';
    }

    for( auto row : grid )
    {
        size_t i = row.find_last_not_of(" ");
        std::cout << row.substr(0,i+1) << "\n";
    }
}


int main( int argc, char ** argv )
{
    // Process arguments.

    while(*++argv)
    {
        std::string arg( *argv );
        if( arg == "-v" )
            gVerbose = true;
        else if( arg == "-h" )
        {
            std::cout << "Usage: day22 [-v] depth tgtx tgty\n";
            return -1;
        }
        else if( !gDepth )
            gDepth = std::stoi( arg );
        else if( !gTargetX )
            gTargetX = std::stoi( arg );
        else if( !gTargetY )
            gTargetY = std::stoi( arg );
    }

    if( !gDepth )
    {
        gDepth = 3339;
        gTargetX = 10;
        gTargetY = 715;
    }

    std::cout << "depth=" << gDepth << ", target=(" << gTargetX << "," << gTargetY << ")\n";

    Coord target(gTargetX, gTargetY);

    // Part 1.

    Cave cave( gDepth, target );
    const char encode[] = "012";
    int sumx = 0;
    for( int y = 0; y <= gTargetY; y++ )
    {
        std::string line;
        for( int x = 0; x <= gTargetX; x++ )
        {
            line += encode[cave.get(x,y)];
            sumx += cave.get(x,y);
        }
//        std::cout << line << "\n";
    }

    std::cout << "Part 1: " << sumx << "\n";

    // OK.
    // Gear, torch, or nothing.
    // Rocky (0)  = gear or torch.
    // Wet (1) = gear or none.
    // Narrow (2) = torch or none.
    //
    // 7 minutes to switch.
    //
    // At each step, we can choose any of the four directions.

    Coord directions[] = { Coord(0,-1), Coord(-1,0), Coord(1,0), Coord(0,1) };

    CoordPlus initial(0,0,TORCH);
    CostMap cost;
    TrackMap  backtrack;
    std::set<CoordPlus> probes;
    std::set<CoordPlus> newprobes;

    cost[initial] = 0;

    // OK, start processing.

    probes.insert( initial );
    int mincost = 99999;
    int mintool = NONE;
    while( !probes.empty() )
    {
#if 0
        std::cout << "New round\n";
#endif
        newprobes.clear();
        for( auto cp : probes )
        {
            int x, y, tool;
            std::tie( x, y, tool ) = cp;

            int dcost = cost[cp];
#if 0
            std::cout << "Checking " << x 
                << " " << y
                << " tool " << tool
                << " cost " << dcost 
                << "\n";
#endif
            if( dcost >= mincost )
                continue;

            for( auto d : directions )
            {
                int nx = x + std::get<0>(d);
                int ny = y + std::get<1>(d);
                //dbgprint( "    ", nx, ny, end=' ' )
                if( nx < 0 || ny < 0 )
                {
                    //dbgprint( "out of bounds" )
                    continue;
                }
                if( nx >= gTargetX+PAD || ny > gTargetY+PAD )
                {
                    //dbgprint( "out of bounds" );
                    continue;
                }

                int newtype = cave.get(nx,ny);
                int newtool = tool;
                int newcost = dcost;

                // dbgprint( newtype, end=' ' )

                // What would be the cost of moving here?

                if( tool != newtype )
                {
                    // We can move directly.
                    newcost += 1;
                    newtool = tool;
                }
                else
                {
                    // dbgprint( "switch", end=' ' )
                    newcost += 8;
                    newtool = 3 - cave.get(x,y) - newtype;
                }

                if( Coord(nx,ny) == target && newtool != TORCH )
                    newcost += 7;

                // Is this better than our last visit?

                Coord newc( nx, ny );
                CoordPlus newx( nx, ny, newtool );

                if( 
                    cost.find(newx) != cost.end() 
                    &&
                    cost[newx] <= newcost
                )
                {
                    //dbgprint( "dead end" );
                    continue;
                }

                //dbgprint( "now", newcost, "using", newtool )
                cost[newx] = newcost;
                backtrack[newx] = cp;

                if( newc == target )
                {
                    if( newcost < mincost )
                    {
                        mincost = newcost;
                        mintool = newtool;
                        std::cout << "New min " << mincost << "\n";
                    }
                }
                else
                    newprobes.insert(newx);
            }
        }

        probes = newprobes;
    }

    CoordPlus winner(gTargetX,gTargetY,mintool);

    std::cout << "Part 2: " << mincost << " " << cost[winner] << "\n";
    
    ShowPlot( backtrack, winner );
}
