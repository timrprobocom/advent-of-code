#include <iostream>
#include <fstream>
#include <sstream>
#include <vector>
#include <string>
#include <tuple>
#include <map>
#include <set>

bool TRACE = false;

// Answer 8.
const char * test[] =  {
"#########\n"
"#b.A.@.a#\n"
"#########\n",

// Answer 86.
"########################\n"
"#f.D.E.e.C.b.A.@.a.B.c.#\n"
"######################.#\n"
"#d.....................#\n"
"########################\n",

// Answer 136.
"#################\n"
"#i.G..c...e..H.p#\n"
"########.########\n"
"#j.A..b...f..D.o#\n"
"########@########\n"
"#k.E..a...g..B.n#\n"
"########.########\n"
"#l.F..d...h..C.m#\n"
"#################""",

// Answer 81.
"########################\n"
"#@..............ac.GI.b#\n"
"###d#e#f################\n"
"###A#B#C################\n"
"###g#h#i################\n"
"########################\n",

// Part 2, answer 72.
"#############\n"
"#g#f.D#..h#l#\n"
"#F###e#E###.#\n"
"#dCba@#@BcIJ#\n"
"#############\n"
"#nK.L@#@G...#\n"
"#M###N#H###.#\n"
"#o#m..#i#jk.#\n"
"#############\n"
};


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


Point movements[4] = { Point(0,-1),Point(0,1),Point(-1,0),Point(1,0) };

typedef std::map<char,std::tuple<Point,int,std::string> > lookupData_t;

struct Maze
{
    std::vector<std::string> m_Maze;
    std::vector<Point> m_Adit;
    int m_Size;

    std::map<char,Point> m_Locations;
    std::map<char,std::map<char,int>> m_Steps;
    std::map<char,std::map<char,std::string>> m_Doors;
    std::map<std::string, int> m_Seen;

    Maze( std::istream && iss )
    {
        for( std::string ln; std::getline( iss, ln );  )
        {
            m_Maze.push_back( ln );
            for( int i = 0; i < ln.size(); i++ )
            {
                if( ln[i] == '@' )
                    m_Adit.emplace_back( i, m_Maze.size() - 1 );
            }
        }
        m_Size = m_Maze.size();
    }

    void print()
    {
        for( auto ln : m_Maze )
            std::cout << ln << "\n";
    }

    void findall( char cfrom, Point & start )
    {
        std::map<Point, std::string> upcoming;
        m_Locations[cfrom] = start;
        upcoming[start] = "";
        std::set<Point> visited;
        int steps = 0;

        while( !upcoming.empty() )
        {
            std::map<Point,std::string> more;
            for( auto && m : upcoming )
            {
                Point cur = m.first;
                std::string & intheway = m.second;

                char ch = at(cur);
                if( islower(ch) && steps )
                {
                    m_Locations[ch] = cur;
                    m_Steps[cfrom][ch] = steps;
                    m_Doors[cfrom][ch] = intheway;
                    m_Steps[ch][cfrom] = steps;
                    m_Doors[ch][cfrom] = intheway;
                }
                if( isupper(ch) )
                    intheway += ch;
                visited.insert( cur );
                for( auto & facing : movements )
                {
                    Point next = cur + facing;
                    char ch = at(next);
                    if( visited.count(next) || ch == '#' )
                        continue;
                    more[next] = intheway;
                }
            }
            upcoming = more;
            steps ++;
        }
    }

    char at( const Point & pt )
    {
        return m_Maze[pt.y][pt.x];
    }

    int search( std::string sitting, std::string found );
};


// Stats key is char, value is (pt,steps,doors in the way)
//
// We need to do a depth-first search to weed out duplicates.

std::string sub(std::string s, int i, char c)
{
    return s.substr(0,i)+c+s.substr(i+1);
}

std::string ssort( std::string s )
{
    std::sort( s.begin(), s.end() );
    return s;
}

#if 0
void bfs( Point start, std::string found )
{
    unchecked = {(start,found): 0 }
    result = 0

    # Keep going as long as there are paths we haven't tested.
    # Because this is "breadth-first", each time through this loop
    # processed all of the paths of a single length.  The next pass
    # will be one step longer.
    while unchecked:
        if TRACE:
            print('Depth',len(next(iter(unchecked.keys()))[1]))
        more = {}
        paths = []

        # For each path that needs to be checked:
        for (sitting, found), steps in unchecked.items():
            paths.append( steps )
            # For each robot:
            for si,s in enumerate(sitting):
                # For each key this robot can see:
                for k,v in stats[s].items():
                    # If we've already picked it up, ignore.
                    if k in found or k < 'a':
                        continue
                    # If any intervening doors are locked, ignore.
                    _, dstep, doors = v
                    if any( d.lower() not in found for d in doors ):
                        continue
                    # If this new path has alread been enumerated, and
                    # this path to the same state is shorter, keep it.
                    newsit = (sub(sitting,si,k),ssort(found+K))
                    if newsit in more and more[newsit] <= steps+dstep:
                        continue
                    more[newsit] = steps+dstep
        # When we have nothing new, we have our answer.
        if not more:
            return min(paths)
        unchecked = more
    return None
}
#endif

int Maze::search( std::string sitting, std::string found )
{
    if( TRACE )
        std::cout << "New search " << sitting << " " << found << "\n";

    found = ssort(found);

    // If we've been in this situation before, we don't need to go again.
    if( m_Seen.find( sitting+found ) != m_Seen.end() )
    {
        return m_Seen[sitting+found];
    }

    std::vector<int> paths;

    // For each robot:
    for( int si = 0; si < sitting.size(); si++ )
    {
        char s = sitting[si];
        if( TRACE ) std::cout << " Checking " << s << "\n";
        // For each key the robot can see:
        for( auto pt : m_Steps )
        {
            if( pt.first < 'a' )
                continue;
            if( TRACE ) std::cout << " Against " << pt.first << " with found " << found << "\n";
            // If we've already picked it up, ignore.
            if( found.find( pt.first ) != found.npos )
                continue;

            // If there's a door in the way without a key, ignore.
            int dstep = m_Steps[s][pt.first];
            std::string doors = m_Doors[s][pt.first];
            if( TRACE ) std::cout << "  dstep " << dstep << "  doors " << doors << "  found " << found << "\n";
            if( std::any_of( 
                doors.begin(), doors.end(),
                [&found](char ch){ return found.find(tolower(ch)) != found.npos;})
            )
                continue;
            // Go explore this path.
            paths.push_back( dstep + search(sub(sitting,si,pt.first), found+pt.first) );
        }
    }
std::cout << sitting << found << " has " << paths.size() << "paths\n";
for( auto & p : paths )
    std::cout << " " << p;
std::cout << "\n";

    int ans = paths.empty() ? 0 : *std::min(paths.begin(),paths.end());
    if( TRACE )
        std::cout << (sitting+found) << ": " << ans << "\n";
    m_Seen[sitting+found] = ans;
    return ans;
}


int main( int argc, char ** argv )
{
    bool do_bfs = false;
    Maze * maze = nullptr;

    while( *++argv )
    {
        if( strcmp(*argv,"trace") == 0 )
            TRACE = true;
        else if( strcmp(*argv,"bfs") == 0 )
            do_bfs = !do_bfs;
        else if( isdigit(*argv[0]) )
            maze = new Maze( std::istringstream(test[*argv[0]-'1']) );
        else
            maze = new Maze( std::ifstream( *argv ));
    }

    maze->print();
    for( auto & pt : maze->m_Adit )
    {
        std::cout << "(" << pt.x << "," << pt.y << ")\n";
    }

    // Find all of the targets.

    for( int i = 0; i < maze->m_Adit.size(); i++ )
    {
        maze->findall( '0'+i, maze->m_Adit[i] );
    }

    // Find the distance betweeen targets.

    for( auto & v : maze->m_Locations )
    {
        std::cout << v.first << ": " << v.second.x << "," << v.second.y << "\n";
        maze->findall( v.first, v.second );
    }

    for( auto & m : maze->m_Steps )
    {
        for( auto & n : m.second )
        {
            std::cout << m.first << " to " << n.first << ": " << n.second << "\n";
        }
    }

#if 0
    begin = time.time();
#endif
    if( maze->m_Adit.size() == 1 )
        std::cout << "Part 1:" << maze->search( "0", "@" ) << "\n";
    else
        std::cout << "Part 2:" << maze->search( "0123", "@" ) << "\n";
#if 0
    delta = time.time() - begin;
    std::cout << "Elapsed:" << delta << "\n";
#endif
}
