CC = g++
CPP = $(CC)
COMMON_OBJS = main.o

ifdef SystemRoot
  RM = del /Q
  EXE = convertbmpto32.exe
  DEFS  = 
  INCLUDES	= -I. -I$(SDL_HOME)/include
  LIBPATH = -L$(SDL_HOME)/lib
  LIBS = -lmingw32 -lSDLmain -lSDL 
else
  ifeq ($(shell uname), Linux)
    RM = rm -f
    EXE = convertbmpto32
    DEFS = -DSTANDALONE -DHAVE_CONFIG_H -DHAVE_GTK2
    INCLUDES = -I.
    LIBS = -lSDL
    OBJS = $(COMMON_OBJS)
  endif
endif

CFLAGS += -std=c++0x -Wall -Weffc++ -pedantic -U__STRICT_ANSI__ 

#HEADERS = $(wildcard *.hpp)

default: all

all: convertbmpto32

convertbmpto32: $(COMMON_OBJS)
	$(CPP) -o convertbmpto32 *.o $(LIBS) $(LIBPATH)

main.o: main.cpp
	$(CPP) -c -o main.o $(CFLAGS) $(INCLUDES) main.cpp

clean:
	$(RM) *.o $(EXE) core

