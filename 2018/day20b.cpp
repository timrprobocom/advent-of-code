#include <string>
#include <vector>
#include <stack>
#include <map>
#include <set>
#include <fstream>
#include <iostream>

// So, here's the magic.  Rather than build all of the possible strings
// up to this point, pos simply holds the list of coordinates we might be
// at, based on all the alternatives to this point.  When we get an 
// alternative, we start again with the list of starting positions for 
// this set of alternatives.
//
// That's really clever.

typedef uint64_t Coord;

Coord make_coord( int x, int y )
{
    return ((uint64_t)(uint32_t)x) << 32 | (uint32_t)y;
}

int getx( Coord & c )
{
    return (int)(c >> 32);
}

int gety( Coord & c )
{
    return (int)(c&0xffff);
}

Coord add( Coord a, Coord b )
{
    return make_coord( getx(a)+getx(b), gety(a)+gety(b) );
}

class Cell
{
    int x;
    int y;
public:
    int steps;
public:
    Cell( int _x, int _y, int _steps=0 )
        : x(_x)
        , y(_y)
        , steps(_steps)
    {
    }

    Cell * add( int dx, int dy )
    {
        return new Cell( x+dx, y+dy, steps+1 );
    }

    Coord coord()
    {
        return make_coord(x,y);
    }
};

typedef std::map<Coord, Cell*> Maze;
typedef std::set<Cell*> CellSet;

Maze createMaze( std::vector<char> & paths )
{
    Cell * base = new Cell(0,0);
    Maze maze;
    maze[base->coord()] = base;

    // the current positions that we're building on.
    CellSet pos;
    // a stack keeping track of (starts, ends) for groups.
    std::stack<CellSet> stack;
    // current possible starting and ending positions.
    CellSet starts, ends;
    starts.insert( base );
    ends.insert( base );

    static std::map<char, Coord> directions;
    if( directions.empty() )
    {
        directions['N'] = make_coord(0,-1);
        directions['E'] = make_coord(1, 0);
        directions['S'] = make_coord(0, 1);
        directions['W'] = make_coord(-1,0);
    }

    for( auto c : paths )
    {
        std::cout << c;
        switch( c )
        {
            case '|':
                // An alternate: update possible ending points, and restart the group.
                ends.insert( pos.begin(), pos.end() );
                pos = starts;
                break;
            case 'N':
            case 'E':
            case 'S':
            case 'W':
            {
                // Move in a given direction, by updating all of possible positions
                // we might have started at.  Add these edges to the graph.
                Coord dir = directions[c];
                CellSet newpos;
                for( auto cell : pos )
                {
                    Coord maybe = add( cell->coord(), dir );
                    if( maze.find( maybe ) == maze.end() )
                    {
                        newpos.insert( maze[maybe] );
                    }
                    else
                    {
                        Cell * n = cell->add( getx(dir), gety(dir) );
                        newpos.insert( n );
                        maze[maybe] = n;
                    }
                }
                pos = newpos;
                break;
            }
            case '(':
                // Start of group.  Push the current starting set so we can use
                // it later, and start a new group.
                stack.push( starts );
                stack.push( ends );
                starts = pos;
                ends.clear();
                break;
            case ')':
                // End of group.  Add the current positions as possible endpoints,
                // and pop the last positions off the stack.
                starts = stack.top();
                stack.pop();
                ends = stack.top();
                stack.pop();
                ends.insert( pos.begin(), pos.end() );
                break;
        }
    }
    std::cout << "Maze has " << maze.size() << "\n";
    return maze;
}


int main()
{
    // Build the graph of all possible movements.


    std::vector<char> inp(10000);
    std::cin.read( inp.data(), inp.size() );
    inp.resize( std::cin.gcount() );

    Maze graph = createMaze( inp );

    std::vector<int> lengths;
    for( auto v : graph )
    {
        lengths.push_back( v.second->steps );
    }
    std::cout <<  "Part 1: " << *std::max_element(lengths.begin(), lengths.end() ) << "\n";
//    print( "Part 2:", sum(1 for pt in graph.values() if pt.steps >= 1000) )
}
