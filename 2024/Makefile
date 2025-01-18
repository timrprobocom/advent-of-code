# vim: sw=8 ts=8 noet:

ifndef windir
O = .o
EXE =
CPPFLAGS = --std=c++17
CXX = g++
LIBS = -llapack
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
OBJS = $(subst .cpp,.$O,$(subst .rs,.$O,$(SRCS)))
EXES = $(subst .cpp,$(EXE),$(subst .rs,$(EXE),$(SRCS)))

%$(EXE): %.cpp
	$(COMPILE.cpp) $(OUTPUT_OPTION) $< $(LIBS)

%$(EXE): %.rs
	rustc $<

all:	$(EXES)

clean:
	rm $(EXES)
