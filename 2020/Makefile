# vim: sw=8 ts=8 noet:

ifndef windir
O = .o
EXE =
CPPFLAGS = --std=c++11
CXX = g++
LIBS = -lgmpxx -lgmp
else
O = .obj
EXE = .exe
CPPFLAGS = -EHsc
OUTPUT_OPTION = -Fe$@
CXX = cl
endif

COMPILE.cpp = $(CXX) $(CPPFLAGS)

SRCS = $(wildcard *.cpp)
OBJS = $(SRCS:.cpp=$O)
EXES = $(SRCS:.cpp=$(EXE))

%$(EXE): %.cpp
	$(COMPILE.cpp) $(OUTPUT_OPTION) $< $(LIBS)

all:	$(EXES)

day18.exe: day18.cpp day18-1.h day18-2.h

day18-1.h:	day18.txt
	sed -e "s/[0-9]/N(&)/g" -e "s/\*/-/g" -e "s/$$/,/" $< > $*.h

day18-2.h:	day18.txt
	sed -e "s/[0-9]/M(&)/g" -e "s/\*/-/g" -e "s/+/*/g" -e "s/$$/,/" $< > $*.h
