um: um.o
	g++ -g $< -o $@

um.o: um.cpp um.h
	g++ -g -c -pthread $< -o $@

clean: 
	$(RM) um um.o

all: um

.PHONY: clean all
