# vim: sw=8 ts=8 noet:

ifndef windir
O = .o
EXE =
CXX = g++
CPPFLAGS = --std=c++17 -O2
LIBS = -llapack
else
O = .obj
EXE = .exe
CXX = cl
CPPFLAGS = -EHsc
OUTPUT_OPTION = -Fe$@
endif

COMPILE.cpp = $(CXX) $(CPPFLAGS)

SRCS = $(wildcard *.cpp)
SRCS += $(wildcard *.rs)
OBJS = $(subst .cpp,.$O,$(subst .rs,.$O,$(SRCS)))
EXES = $(subst .cpp,$(EXE),$(subst .rs,$(EXE),$(SRCS)))

%$(EXE): %.cpp utils.h
	$(COMPILE.cpp) $(OUTPUT_OPTION) $< $(LIBS)

%$(EXE): %.rs
	rustc $<

all:	$(EXES)

clean:
	rm $(EXES)
