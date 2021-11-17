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
