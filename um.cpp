#include "um.h"
#include <iostream>

int main(int argc, char** argv) {
    if (argc < 2) {
        std::cerr << "Usage: ./um file.um(z)" << std::endl;
        exit(0);
    }

    std::string infile(argv[1]);
    UM um(infile);
    
    exit(1);
}
