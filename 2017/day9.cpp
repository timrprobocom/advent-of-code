#include <fstream>
#include <iostream>
#include <string>
#include <queue>

typedef std::queue<char> charQueue;

int Parse( charQueue & line, int nest = 0 )
{
    int score = nest;
    bool escape = false;
    bool garbage = false;
    while( !line.empty() )
    {
        char c = line.front();
        line.pop();

        if( escape )
            escape = false;
        else if( c == '!' )
            escape = true;
        else if( garbage )
            garbage = c != '>';
        else if( c == '<' )
            garbage = true;
        else if( c == '{' )
            score += Parse(line, nest+1);
        else if( c == '}' )
            break;
    }
    return score;
}

int Parse( const char * sz )
{
    charQueue q;
    while( *sz )
        q.push( *sz++ );
    return Parse( q );
}

int Parse2( charQueue & line )
{
    int score = 0;
    bool escape = false;
    bool garbage = false;
    while( !line.empty() )
    {
        char c = line.front();
        line.pop();

        if( escape )
            escape = false;
        else if( c == '!' )
            escape = true;
        else if( garbage )
        {
            if( c == '>' )
                garbage = false;
            else
                score++;
        }
        else if( c == '<' )
            garbage = true;
        else if( c == '{' )
            score += Parse2(line);
        else if( c == '}' )
            break;
    }
    return score;
}

int Parse2( const char * sz )
{
    charQueue q;
    while( *sz )
        q.push( *sz++ );
    return Parse2( q );
}

void test()
{
    std::cout << Parse( "{}" ) << "\n";
    std::cout << Parse( "{{{}}}" ) << "\n";
    std::cout << Parse( "{{},{}}" ) << "\n";
    std::cout << Parse( "{{{},{},{{}}}}" ) << "\n";
    std::cout << Parse( "{<a>,<a>,<a>,<a>}" ) << "\n";
    std::cout << Parse( "{{<ab>},{<ab>},{<ab>},{<ab>}}" ) << "\n";
    std::cout << Parse( "{{<!!>},{<!!>},{<!!>},{<!!>}}" ) << "\n";
    std::cout << Parse( "{{<a!>},{<a!>},{<a!>},{<ab>}}" ) << "\n";
}

void live()
{
    std::ifstream is("day9.txt");
    charQueue q;
    while( !is.eof() )
    {
        char c;
        is >> c;
        q.push(c);
    }
    std::cout << Parse( q ) << "\n";
}

void test2()
{
    std::cout << Parse2( "<>" ) << "\n";
    std::cout << Parse2( "<random characters>" ) << "\n";
    std::cout << Parse2( "<<<<>" ) << "\n";
    std::cout << Parse2( "<{!>}>" ) << "\n";
    std::cout << Parse2( "<!!>" ) << "\n";
    std::cout << Parse2( "<!!!>>" ) << "\n";
    std::cout << Parse2( "<{o\"i!a,<{i<a>" ) << "\n";
}

void live2()
{
    std::ifstream is("day9.txt");
    charQueue q;
    while( !is.eof() )
    {
        char c;
        is >> c;
        q.push(c);
    }
    std::cout << Parse2( q ) << "\n";
}


int
main()
{
    test();
    live();
    test2();
    live2();
}
