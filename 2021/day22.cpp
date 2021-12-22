#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <set>
#include <algorithm>
#include <numeric>

using namespace std;

const char * test1 = 
    "on x=-20..26,y=-36..17,z=-47..7\n"
    "on x=-20..33,y=-21..23,z=-26..28\n"
    "on x=-22..28,y=-29..23,z=-38..16\n"
    "on x=-46..7,y=-6..46,z=-50..-1\n"
    "on x=-49..1,y=-3..46,z=-24..28\n"
    "on x=2..47,y=-22..22,z=-23..27\n"
    "on x=-27..23,y=-28..26,z=-21..29\n"
    "on x=-39..5,y=-6..47,z=-3..44\n"
    "on x=-30..21,y=-8..43,z=-13..34\n"
    "on x=-22..26,y=-27..20,z=-29..19\n"
    "off x=-48..-32,y=26..41,z=-47..-37\n"
    "on x=-12..35,y=6..50,z=-50..-2\n"
    "off x=-48..-32,y=-32..-16,z=-15..-5\n"
    "on x=-18..26,y=-33..15,z=-7..46\n"
    "off x=-40..-22,y=-38..-28,z=23..41\n"
    "on x=-16..35,y=-41..10,z=-47..6\n"
    "off x=-32..-23,y=11..30,z=-14..3\n"
    "on x=-49..-5,y=-3..45,z=-29..18\n"
    "off x=18..30,y=-20..-8,z=-3..13\n"
    "on x=-41..9,y=-7..43,z=-33..15\n"
    "on x=-54112..-39298,y=-85059..-49293,z=-27449..7877\n"
    "on x=967..23432,y=45373..81175,z=27513..53682\n";

const char * test2 = 
    "on x=-5..47,y=-31..22,z=-19..33\n"
    "on x=-44..5,y=-27..21,z=-14..35\n"
    "on x=-49..-1,y=-11..42,z=-10..38\n"
    "on x=-20..34,y=-40..6,z=-44..1\n"
    "off x=26..39,y=40..50,z=-2..11\n"
    "on x=-41..5,y=-41..6,z=-36..8\n"
    "off x=-43..-33,y=-45..-28,z=7..25\n"
    "on x=-33..15,y=-32..19,z=-34..11\n"
    "off x=35..47,y=-46..-34,z=-11..5\n"
    "on x=-14..36,y=-6..44,z=-16..29\n"
    "on x=-57795..-6158,y=29564..72030,z=20435..90618\n"
    "on x=36731..105352,y=-21140..28532,z=16094..90401\n"
    "on x=30999..107136,y=-53464..15513,z=8553..71215\n"
    "on x=13528..83982,y=-99403..-27377,z=-24141..23996\n"
    "on x=-72682..-12347,y=18159..111354,z=7391..80950\n"
    "on x=-1060..80757,y=-65301..-20884,z=-103788..-16709\n"
    "on x=-83015..-9461,y=-72160..-8347,z=-81239..-26856\n"
    "on x=-52752..22273,y=-49450..9096,z=54442..119054\n"
    "on x=-29982..40483,y=-108474..-28371,z=-24328..38471\n"
    "on x=-4958..62750,y=40422..118853,z=-7672..65583\n"
    "on x=55694..108686,y=-43367..46958,z=-26781..48729\n"
    "on x=-98497..-18186,y=-63569..3412,z=1232..88485\n"
    "on x=-726..56291,y=-62629..13224,z=18033..85226\n"
    "on x=-110886..-34664,y=-81338..-8658,z=8914..63723\n"
    "on x=-55829..24974,y=-16897..54165,z=-121762..-28058\n"
    "on x=-65152..-11147,y=22489..91432,z=-58782..1780\n"
    "on x=-120100..-32970,y=-46592..27473,z=-11695..61039\n"
    "on x=-18631..37533,y=-124565..-50804,z=-35667..28308\n"
    "on x=-57817..18248,y=49321..117703,z=5745..55881\n"
    "on x=14781..98692,y=-1341..70827,z=15753..70151\n"
    "on x=-34419..55919,y=-19626..40991,z=39015..114138\n"
    "on x=-60785..11593,y=-56135..2999,z=-95368..-26915\n"
    "on x=-32178..58085,y=17647..101866,z=-91405..-8878\n"
    "on x=-53655..12091,y=50097..105568,z=-75335..-4862\n"
    "on x=-111166..-40997,y=-71714..2688,z=5609..50954\n"
    "on x=-16602..70118,y=-98693..-44401,z=5197..76897\n"
    "on x=16383..101554,y=4615..83635,z=-44907..18747\n"
    "off x=-95822..-15171,y=-19987..48940,z=10804..104439\n"
    "on x=-89813..-14614,y=16069..88491,z=-3297..45228\n"
    "on x=41075..99376,y=-20427..49978,z=-52012..13762\n"
    "on x=-21330..50085,y=-17944..62733,z=-112280..-30197\n"
    "on x=-16478..35915,y=36008..118594,z=-7885..47086\n"
    "off x=-98156..-27851,y=-49952..43171,z=-99005..-8456\n"
    "off x=2032..69770,y=-71013..4824,z=7471..94418\n"
    "on x=43670..120875,y=-42068..12382,z=-24787..38892\n"
    "off x=37514..111226,y=-45862..25743,z=-16714..54663\n"
    "off x=25699..97951,y=-30668..59918,z=-15349..69697\n"
    "off x=-44271..17935,y=-9516..60759,z=49131..112598\n"
    "on x=-61695..-5813,y=40978..94975,z=8655..80240\n"
    "off x=-101086..-9439,y=-7088..67543,z=33935..83858\n"
    "off x=18020..114017,y=-48931..32606,z=21474..89843\n"
    "off x=-77139..10506,y=-89994..-18797,z=-80..59318\n"
    "off x=8476..79288,y=-75520..11602,z=-96624..-24783\n"
    "on x=-47488..-1262,y=24338..100707,z=16292..72967\n"
    "off x=-84341..13987,y=2429..92914,z=-90671..-1318\n"
    "off x=-37810..49457,y=-71013..-7894,z=-105357..-13188\n"
    "off x=-27365..46395,y=31009..98017,z=15428..76570\n"
    "off x=-70369..-16548,y=22648..78696,z=-1892..86821\n"
    "on x=-53470..21291,y=-120233..-33476,z=-44150..38147\n"
    "off x=-93533..-4276,y=-16170..68771,z=-104985..-24507\n";

bool DEBUG = false;

typedef vector<int> Cube;

struct Order {
    bool state;
    Cube cube;
};

typedef vector<Cube> Cubes;
typedef vector<Order> Orders;

void parse( istream & incoming, Orders & orders )
{
    // Lets parse it char by char.

    char c;
    orders.clear();
    string number;
    Order build;
    while( incoming.get(c) )
    {
        switch(c)
        {
            case 'f':
                build.state = false;
                break;
            case 'n':
                build.state = true;
                break;
            case ' ':
                number.clear();
                build.cube.clear();
                break;
            case '\n':
                if( !number.empty() )
                {
                    build.cube.push_back( stoi(number) );
                    number.clear();
                }
                // Make the ends exclusive.
                build.cube[1] += 1;
                build.cube[3] += 1;
                build.cube[5] += 1;
                orders.push_back( build );
                break;
            case '-': case '0': case '1': case '2':
            case '3': case '4': case '5': case '6':
            case '7': case '8': case '9':
                number.push_back( c );
                break;
            case '.':
            case ',':
                if( !number.empty() )
                    build.cube.push_back( stoi(number) );
                number.clear();
                break;
        }
    }
    // The data file does not have a closing newline.
    if( !number.empty() )
    {
        build.cube.push_back( stoi(number) );
        build.cube[1] += 1;
        build.cube[3] += 1;
        build.cube[5] += 1;
        orders.push_back( build );
    }
}


// For part 1, we use a 3D matrix and set the lights using ones and zeros.

int part1( Orders & orders )
{
    static int8_t world[101][101][101];
    for( auto && order : orders )
    {
        int xlo = max(-50,order.cube[0])+50;
        int xhi = min( 51,order.cube[1])+50;
        int ylo = max(-50,order.cube[2])+50;
        int yhi = min( 51,order.cube[3])+50;
        int zlo = max(-50,order.cube[4])+50;
        int zhi = min( 51,order.cube[5])+50;
        if( xlo > 101 || xhi < 0 || ylo > 101 || yhi < 0 || zlo > 101 || zhi < 0)
            continue;

        for( int z = zlo; z < zhi; z++ )
            for( int y = ylo; y < yhi; y++ )
                for( int x = xlo; x < xhi; x++ )
                    world[z][y][x] = order.state;
    }

    return std::accumulate( &world[0][0][0], &world[101][0][0], 0 );
}

// For part 2 we need to track lit regions, not cells.  For each new cube coming,
// we scan the whole list of existing cubes.  If there is an intersect, we
// create as many as 6 new subcubes that prepresent the sections that do not
// intersect.

bool intersects( const Cube & cube1, const Cube & cube2 )
{
    return
        cube2[1] > cube1[0] &&
        cube2[0] < cube1[1] &&
        cube2[3] > cube1[2] &&
        cube2[2] < cube1[3] &&
        cube2[5] > cube1[4] &&
        cube2[4] < cube1[5];
}

// Intersect all cubes with the new one.  We replace the
// cubes list with a new list.

void cubeintersect( Cubes & allcubes, const Cube & master )
{
    Cubes newcubes;

    for( auto && cube : allcubes )
    {
        if( !intersects( cube, master ) )
        {
            newcubes.push_back( cube );
        }
        else
        {
            // We basically cut off any slices on the end that don't 
            // intersect and add them.

            if( cube[0] < master[0] )
            {
                newcubes.emplace_back(Cube{
                    cube[0], master[0],
                    cube[2], cube[3],
                    cube[4], cube[5]
                });
                cube[0] = master[0];
            }

            if( cube[1] > master[1] )
            {
                newcubes.emplace_back(Cube{
                    master[1], cube[1],
                    cube[2], cube[3],
                    cube[4], cube[5]
                });
                cube[1] = master[1];
            }


            if( cube[2] < master[2] )
            {
                newcubes.emplace_back(Cube{
                    cube[0], cube[1],
                    cube[2], master[2],
                    cube[4], cube[5]
                });
                cube[2] = master[2];
            }

            if( cube[3] > master[3] )
            {
                newcubes.emplace_back(Cube{
                    cube[0], cube[1],
                    master[3], cube[3],
                    cube[4], cube[5]
                });
                cube[3] = master[3];
            }



            if( cube[4] < master[4] )
            {
                newcubes.emplace_back(Cube{
                    cube[0], cube[1],
                    cube[2], cube[3],
                    cube[4], master[4]
                });
                cube[4] = master[4];
            }

            if( cube[5] > master[5] )
            {
                newcubes.emplace_back(Cube{
                    cube[0], cube[1],
                    cube[2], cube[3],
                    master[5], cube[5]
                });
                cube[5] = master[5];
            }
        }
    }

    allcubes.swap( newcubes );
}

// Compute the number of lit cells.

int64_t sumall( const Cubes & cubes )
{
    int64_t sumx = 0;
    for( auto && cube : cubes )
    {
        sumx += 
            int64_t(cube[1]-cube[0]) *
            int64_t(cube[3]-cube[2]) *
            int64_t(cube[5]-cube[4]);
    }
    return sumx;
}

int64_t part2( Orders & orders )
{
    Cubes cubes;
    for( auto && order : orders )
    {
        cubeintersect( cubes, order.cube );
        if( order.state )
            cubes.push_back( order.cube );
    }

    return sumall(cubes);
}

// Do part 1 using part 2's scheme.

int64_t part12( const Orders & orders )
{
    Cubes cubes;
    for( auto && order : orders )
    {
        Cube cube = order.cube;
        if( 
            cube[0] > 51 || cube[1] < -50 || 
            cube[2] > 51 || cube[3] < -50 || 
            cube[4] > 51 || cube[5] < -50 )
            continue;
        cube[0] = max(-50,cube[0]);
        cube[1] = min( 51,cube[1]);
        cube[2] = max(-50,cube[2]);
        cube[3] = min( 51,cube[3]);
        cube[4] = max(-50,cube[4]);
        cube[5] = min( 51,cube[5]);
        cubeintersect( cubes, cube );
        if( order.state )
            cubes.push_back( order.cube );
    }

    return sumall(cubes);
}

int main( int argc, char ** argv )
{
    istringstream data1;
    istringstream data2;
    while( *++argv )
    {
        if( strcmp(*argv, "debug") == 0 )
            DEBUG = true;
        else if( strcmp(*argv, "test") == 0 )
        {
            data1.str( test1 );
            data2.str( test2 );
        }
    }

    if( data1.str().empty() )
    {
        stringstream buffer;
        buffer << ifstream("day22.txt").rdbuf();
        data1.str( buffer.str() );
        data2.str( buffer.str() );
    }

    Orders orders;
    parse(data1, orders);
    cout << "Part 1: " << part1(orders) << "\n";
    cout << "Part 1: " << part12(orders) << "\n";

    parse(data2, orders);
    cout << "Part 2: " << part2(orders) << "\n";
}

