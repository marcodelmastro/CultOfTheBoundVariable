#ifndef UM_H
#define UM_H

#include <vector>
#include <string>
#include <fstream>
#include <iostream>

class UM {
  
 private:

  uint32_t i = 0;
  uint32_t reg[8] = {};
  uint32_t status;
  std::vector<std::vector<uint32_t>*> mem;
  std::vector<uint32_t> freed;

  std::vector<uint32_t>* readProg(std::string infile);

 public:

  explicit UM(std::string infile);
  ~UM();
  void run();

};

UM::UM(std::string infile) {
  // read program from file, inizialize memory
  std::vector<uint32_t>* program = readProg(infile);
  mem.push_back(program);
}

UM::~UM(){}

void UM::run() {
  status = 1; // running!
  while (status>0) {

    if (i>=mem[0]->size()) {
      std::cerr << " ** Reached end of program **" << std::endl;
      return;
    }

    // get instruction from program array
    uint32_t p = mem[0]->at(i);

    // decode instructions
    uint32_t op = p >> (32-4);
    if (op==13) {
      uint32_t a = p >> (32-4-3) & 0b111;
      uint32_t v = p & 0b00000001111111111111111111111111;
      std::cout << op << " " << a << " " << v << std::endl;
      //UM.operation[op](self,a,v)
    } else {
      uint32_t a = (p & 0b111000000) >> 6;
      uint32_t b = (p & 0b000111000) >> 3;
      uint32_t c = (p & 0b000000111) >> 0;
      std::cout << op << " " << a << " " << b << " " << c << std::endl;
      //UM.operation[op](self,a,b,c)
    }

    i++;
  }
}

std::vector<uint32_t>* UM::readProg(std::string infile) {
    std::ifstream input(infile.c_str(), std::ios::binary);
    std::vector<unsigned char> buffer((std::istreambuf_iterator<char>(input)), std::istreambuf_iterator<char>());
    auto program = new std::vector<uint32_t>();
    for (uint32_t i = 0; i < buffer.size() / 4; i++) {
      const uint8_t b0 = buffer[i*4+3];
      const uint8_t b1 = buffer[i*4+2];
      const uint8_t b2 = buffer[i*4+1];
      const uint8_t b3 = buffer[i*4];
      uint32_t w = (b0 << 0) | (b1 << 8) | (b2 << 16) | (b3 << 24);
      program->push_back(w);
    }
    return program;
}

#endif // UM_H
