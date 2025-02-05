import os
import subprocess
import time

# python c++ go

# Python is slowest, then unoptimized C++, then go and optimized C++ are about the same.

def fetch(cmd):
    return subprocess.run( cmd, check=True, stdout=subprocess.PIPE).stdout.decode()

def prep(file, ext):
    if ext == '.cpp':
        subprocess.run(['g++', '--std=c++17', '-O3', '-o', file, file+ext, '-llapack'])
    elif ext == '.go':
        subprocess.run(['go', 'build', file+ext] )

def run(file, ext):
    if ext == '.py':
        return fetch(['python', fn+ext])
    else:
        return fetch(['./'+fn])

print('Python'.ljust(30), 'C++'.ljust(30), 'Go')

for day in range(1,26):
    fn = f'day{day:02d}'
    gather = []
    times = []
    for lang in '.py','.cpp','.go':
        if os.path.exists(fn+lang):
            prep( fn, lang )
            before = time.time()
            s = run( fn, lang )
            times.append( time.time() - before )
            gather.append( s.splitlines() )

    print(fn)
    for lns in zip(*gather):
        for ln in lns:
            print(ln.ljust(30),end='')
        print()
    for t in times:
        print( ('%10.3f'%t).ljust(30), end='')
    print()

