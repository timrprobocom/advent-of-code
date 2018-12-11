#include <fstream>
#include <iostream>
#include <list>

int main()
{
    std::list<int> buffer;
    buffer.push_back( 0 );
#if 0
    int data = 3;
    int rounds = 2017;
#else
    int data = 328;
    int rounds = 5000000;
#endif
    std::list<int>::iterator posn = buffer.begin();

    for( int i = 1; i <= rounds; i++ )
    {
        if( i % 100000 == 0 )
        {
            std::cout << i << "\r";
            std::cout.flush();
        }
        for( int m = 0; m < data+1; m++ )
        {
            if( posn == buffer.end() )
                posn = buffer.begin();
            posn++;
        }
        posn = buffer.insert( posn, i );
#if 0
        for( auto && p = buffer.begin(); p != buffer.end(); p++ )
            std::cout << *p << ", ";
        std::cout << std::endl;
#endif
    }

    auto p = std::find( buffer.begin(), buffer.end(), 0 );

    std::cout << "\n";
    std::cout << *p << ", ";
    p++;
    std::cout << *p << "\n";

    p = std::find( buffer.begin(), buffer.end(), 2017 );

    std::cout << *p << ", ";
    p++;
    std::cout << *p << "\n";
}

