#pragma once
#include <iostream>
#include <thread>
#include <deque>
#include <memory>
#include <vector>
#include <chrono>

using namespace std;

// The IntCode computer.

static int count = 0;

template<typename T>
class Program
{
    int id;
    vector<T> m_Program;
    int pc;
    int m_Modes;
    shared_ptr<deque<T> > m_Input;
    shared_ptr<deque<T> > m_Output;
    T m_Final;
    int m_Rbase;
	thread m_MyThread;
    
public:
    Program( vector<T> pgm )
        : id( ::count++ )
        , m_Program( pgm )
        , m_Input( make_shared<deque<T>>() )
        , m_Output( make_shared<deque<T>>() )
        , pc( 0 )
        , m_Rbase( 0 )
    {
    }

    void push( T val )
    {
        m_Input->push_back( val );
    }

    T pop()
    {
        T p = m_Output->front();
        m_Output->pop_front();
        return p;
    }

    T Final() const 
	{
		return m_Final;
	}

    vector<T> dump()
    {
        vector<T> q;
        q.insert( q.begin(), m_Output->begin(), m_Output->end() );
        return q;
    }

    static void connect( Program & producer, Program & consumer)
    {
        consumer.m_Input = producer.m_Output;
    }
 
    int opcode()
    {
        int opc = m_Program[pc];
        m_Modes = opc/100;
        if( TRACE )
            cout << id << ": At " << pc << ": " << opc << "\n";
        pc++;
        return opc % 100;
    }

    int nextmode()
    {
        int p = m_Modes % 10;
        m_Modes /= 10;
        return p;
    }

    void verify(int loc)
    {
        if( loc >= m_Program.size() )
        {
            m_Program.resize( loc+1 );
            if( TRACE )
                cout << "Extending memory to " << loc << "\n";
        }
    }

    T fetch()
    {
        int mode = nextmode();
        T operand = m_Program[pc++];
        T val = 0;
        switch( mode )
        {
            case 0:
                verify(operand);
                val = m_Program[operand];
                break;
            case 1:
                val = operand;
                break;
            case 2:
                verify(operand+m_Rbase);
                val = m_Program[operand+m_Rbase];
                break;
        }
        if( TRACE )
            cout << id  << ": fetch[" << mode << "] " << operand << " = " << val << "\n";
        return val;
    }

    void store( T n )
    {
        int mode = nextmode();
        T operand = m_Program[pc++];
        if( TRACE )
            cout << id << ": store[" << mode << "] " << n << " at " << operand << "\n";
        switch( mode )
        {
            case 0:
                verify(operand);
                m_Program[operand] = n;
                break;
            case 1:
                cout << "EXPLODE\n";
                return;
            case 2:
                verify(operand+m_Rbase);
                m_Program[operand+m_Rbase] = n;
                break;
        }
    }

    void jump() 
    {
        pc = fetch();
    }

    void skip()
    {
        pc ++;
    }

    Program<T> & run()
    {
        T ip;
        for( ;; )
        {
            switch( opcode() )
            {
                case 1:
                    store( fetch() + fetch() );
                    break;
                case 2:
                    store( fetch() * fetch() );
                    break;
                case 3:
                    while( m_Input->empty() )
                        this_thread::sleep_for(chrono::microseconds(500));
                     ip = m_Input->front();
                     m_Input->pop_front();
                     if( TRACE )
                         cout << id << ": input " << ip << "\n";
                     store( ip );
                     break;
                case 4:
                    ip = fetch();
                    m_Final = ip;
                    m_Output->push_back( ip );
                    if( TRACE )
                        cout << id << ": output " << ip << "\n";
                    break;
                case 5: // JT
                    if( fetch() )
                        jump();
                    else
                        skip();
                    break;
                case 6: // JF
                    if( !fetch() )
                        jump();
                    else
                        skip();
                    break;
                case 7: // JLT
                    store( (int)(fetch() < fetch()));
                    break;
                case 8: // JE
                    store( (int)(fetch() == fetch()));
                    break;
                case 9: // set rbase
                    m_Rbase += fetch();
                    break;
                case 99: // halt
                    return *this;
                default:
                    cout << "Explode, pc=" << pc << ", pgm=" << "\n";
                    return *this;
            }
        }
    }

	void start() {
		m_MyThread = thread( &Program::run, this );
	}
	
	void wait() {
		m_MyThread.join();
	}
};

