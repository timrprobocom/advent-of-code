# vim: sw=8 ts=8 noet:

ifndef windir
O = .o
EXE =
CPPFLAGS = --std=c++11
else
O = .obj
EXE = .exe
CPPFLAGS = -EHsc
OUTPUT_OPTION = -Fe$@
endif

SRCS = $(wildcard *.cpp)
OBJS = $(SRCS:.cpp=$O)
EXES = $(SRCS:.cpp=$(EXE))

%$(EXE): %.cpp
	cl $(CPPFLAGS) $(OUTPUT_OPTION) $<

all:	$(EXES)


