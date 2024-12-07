# vim: sw=8 ts=8 noet:

ifndef windir
O = .o
EXE =
CPPFLAGS = --std=c++17
CXX = g++
LIBS = 
else
O = .obj
EXE = .exe
CPPFLAGS = -EHsc
OUTPUT_OPTION = -Fe$@
CXX = cl
endif

COMPILE.cpp = $(CXX) $(CPPFLAGS)

SRCS = $(wildcard *.cpp)
SRCS += $(wildcard *.rs)
OBJS = $(SRCS:.cpp=$O)
OBJS += $(SRCS:.rs=$O)
EXES = $(SRCS:.cpp=$(EXE))
EXES += $(SRCS:.rs=$(EXE))

%$(EXE): %.cpp
	$(COMPILE.cpp) $(OUTPUT_OPTION) $< $(LIBS)

%$(EXE): %.rs
	rustc $<

all:	$(EXES)

