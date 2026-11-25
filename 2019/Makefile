# vim: sw=8 ts=8 noet:

ifndef windir
UNAME = $(shell uname -s)
O = .o
EXE =
CPPFLAGS = --std=c++11
CXX = g++
LIBS = -lgmpxx -lgmp
#LIBS =
ifeq ($(UNAME),Darwin)
CPPFLAGS += -I/opt/homebrew/include
LIBS += -L/opt/homebrew/lib
endif
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


