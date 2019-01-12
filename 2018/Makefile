# vim: sw=8 ts=8 noet:

ifndef windir
O = .o
EXE =
else
O = .obj
EXE = .EXE
endif

CPPFLAGS = --std=c++11
SRCS = $(wildcard *.cpp)
OBJS = $(SRCS:.cpp=$O)
EXES = $(SRCS:.cpp=$(EXE))

%.$O: %.cpp
	cl $(CPPFLAGS) $(OUTPUT_OPTION) $<

%: %.$O
	$(LINK)$@ $(LDFLAGS) $< $(LIBS)

all:	$(EXES)


