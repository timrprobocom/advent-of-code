#include <fstream>
#include <iostream>
#include <vector>
#include <string>
#include <map>

const char * live[] = {
    "set b 65",
    "set c b",
    "jnz a 2",
    "jnz 1 5",
    "mul b 100",
    "sub b -100000",
    "set c b",
    "sub c -17000",
    "set f 1",
    "set d 2",
    "set e 2",
    "set g d",
    "mul g e",
    "sub g b",
    "jnz g 2",
    "set f 0",
    "sub e -1",
    "set g e",
    "sub g b",
    "jnz g -8",
    "sub d -1",
    "set g d",
    "sub g b",
    "jnz g -13",
    "jnz f 2",
    "sub h -1",
    "set g b",
    "sub g c",
    "jnz g 2",
    "jnz 1 3",
    "sub b -17",
    "jnz 1 -23",
    nullptr
};

enum opcode_t {
    opWhat,
    opSet,
    opJnz,
    opMul,
    opSub
};

struct instruction_t {
    opcode_t opcode;
    char op1;
    bool op2_is_reg;
    int op2;
};

typedef std::vector<instruction_t> code_t;
typedef std::map<char,int64_t> registerFile_t;

void fillRegisters( registerFile_t & regs )
{
    regs['a'] = 0;
    regs['b'] = 0;
    regs['c'] = 0;
    regs['d'] = 0;
    regs['e'] = 0;
    regs['f'] = 0;
    regs['g'] = 0;
    regs['h'] = 0;
    regs['1'] = 1;
    regs['p'] = 0;
}


instruction_t parse( std::string ln )
{
    static std::map<std::string, opcode_t> opcodeMap;
    if( opcodeMap.empty() )
    {
        opcodeMap["set"] = opSet;
        opcodeMap["jnz"] = opJnz;
        opcodeMap["mul"] = opMul;
        opcodeMap["sub"] = opSub;
    }

    instruction_t instr;

    int i1 = ln.find(' ');
    int i2 = ln.find(' ', i1+1);
    std::string opcode = ln.substr( 0, i1 );
    instr.opcode = opcodeMap[ opcode ];
    instr.op1 = ln[i1+1];
    instr.op2_is_reg = !((ln[i2+1] >= '0'&& ln[i2+1] <= '9') || ln[i2+1] == '-');

    if( instr.op2_is_reg )
    {
        instr.op2 = ln[i2+1];
    }
    else
    {
        instr.op2 = std::stoi( ln.substr(i2+1) );
    }

    return instr;
}


code_t compileProgram( const char ** program )
{
    code_t code;

    for( ; *program; program++ )
    {
        if( **program != '#' )
            code.push_back( parse( *program ) );
    }

    return code;
}


int lookup( registerFile_t & regs, instruction_t * instr )
{
    if( instr->op2_is_reg )
        return regs[instr->op2];
    else
        return instr->op2;
}

void summarize( registerFile_t & registers )
{
    std::cout 
        << " b:" << registers['b']
        << " c:" << registers['c'] 
        << " d:" << registers['d']
        << " e:" << registers['e']
        << " h:" << registers['h']
        << "\n";
}


int main()
{
    code_t code = compileProgram(live);
    registerFile_t registers;
    fillRegisters( registers );
    registers['a'] = 1;

    // Go.

    int muls = 0;
    while( registers['p'] < code.size() )
    {
        instruction_t * instr = &code[registers['p']];
        int op2 = (instr->op2_is_reg)
            ? registers[instr->op2]
            : instr->op2;

        switch( instr->opcode )
        {
            case opSet:
                registers[instr->op1] = op2;
                break;
            case opSub:
                registers[instr->op1] -= op2;
                if( instr->op1 == 'd' )
                    summarize( registers );
                if( instr->op1 == 'h' )
                    std::cout << "h is now " << registers['h'] << "\n";
                break;
            case opMul:
                muls++;
                registers[instr->op1] *= op2;
                break;
            case opJnz:
                if( registers[instr->op1] )
                    registers['p'] += op2 - 1;
                break;
            default:
                break;
        }
        registers['p'] ++;
    }
    std::cout << muls << " multiplies\n";
}
