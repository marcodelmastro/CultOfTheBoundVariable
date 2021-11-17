#ifndef UM_H
#define UM_H

#include <vector>
#include <string>
#include <fstream>
#include <iostream>
#include <map>
#include <functional>

class UM {
  
 private:

  uint32_t i = 0;
  uint32_t reg[8] = {};
  uint32_t status;
  std::vector<std::vector<uint32_t>*> mem;
  std::vector<uint32_t> freed;

  std::vector<uint32_t>* readProg(std::string infile);

  // operators
  void conditional_move(uint32_t a, uint32_t b, uint32_t c);
  void array_index(uint32_t a, uint32_t b, uint32_t c);
  void array_amendment(uint32_t a, uint32_t b, uint32_t c);
  void addition(uint32_t a, uint32_t b, uint32_t c);
  void multiplication(uint32_t a, uint32_t b, uint32_t c);
  void division(uint32_t a, uint32_t b, uint32_t c);
  void not_and(uint32_t a, uint32_t b, uint32_t c);
  void halt(uint32_t a, uint32_t b, uint32_t c);
  void allocation(uint32_t a, uint32_t b, uint32_t c);
  void abandonement(uint32_t a, uint32_t b, uint32_t c);
  void output_(uint32_t a, uint32_t b, uint32_t c);
  void input_(uint32_t a, uint32_t b, uint32_t c);
  void load_program(uint32_t a, uint32_t b, uint32_t c);
  void orthography(uint32_t a, uint32_t v);

 public:

  explicit UM(std::string infile);
  ~UM();
  void run();

};

UM::UM(std::string infile) {
  // read program from file, initialize memory
  //std::vector<uint32_t>* program = readProg(infile);
  auto program = readProg(infile);
  mem.push_back(program);
}

UM::~UM(){}

void UM::conditional_move(uint32_t a, uint32_t b, uint32_t c) {
  if (reg[c]!=0) reg[a] = reg[b];
  return;
}

void UM::array_index(uint32_t a, uint32_t b, uint32_t c) {
  reg[a] = mem[reg[b]]->at(reg[c]);
  return;
}

void UM::array_amendment(uint32_t a, uint32_t b, uint32_t c) {
  mem[reg[a]]->at(reg[b]) = reg[c];
  return;
}

void UM::addition(uint32_t a, uint32_t b, uint32_t c) {
  reg[a] = (reg[b]+reg[c]) & 0xFFFFFFFF;
  return;
}

void UM::multiplication(uint32_t a, uint32_t b, uint32_t c) {
  reg[a] = (reg[b]*reg[c]) & 0xFFFFFFFF;
  return;
}

void UM::division(uint32_t a, uint32_t b, uint32_t c) {
  if ( reg[c]>0 )
    reg[a] = (reg[b]/reg[c]) & 0xFFFFFFFF;
  return;
}

void UM::not_and(uint32_t a, uint32_t b, uint32_t c) {
  reg[a] = (~(reg[b]&reg[c])) & 0xFFFFFFFF;
  return;
}

void UM::halt(uint32_t a, uint32_t b, uint32_t c) {
  status = 0;
  return;
}

void UM::allocation(uint32_t a, uint32_t b, uint32_t c) {
  auto newarray = new std::vector<uint32_t>(reg[c]);
  if ( freed.empty() ) {
    mem.push_back(newarray);
    reg[b] = mem.size()-1;
  } else {
    uint32_t freeadd = freed[0];
    freed.erase(freed.begin());	   
    mem[freeadd] = newarray;
    reg[b] = freeadd;
  }
  return;
}

void UM::abandonement(uint32_t a, uint32_t b, uint32_t c) {
  mem[reg[c]] = NULL;
  freed.push_back(reg[c]);
  return;
}

void UM::output_(uint32_t a, uint32_t b, uint32_t c) {
  std::putchar(static_cast<char>(reg[c]));
  return;
}

void UM::input_(uint32_t a, uint32_t b, uint32_t c) {
  reg[c] = std::getchar();
  //reg[c] = 0xFFFFFFFF;
  return;
}

void UM::load_program(uint32_t a, uint32_t b, uint32_t c) {
  if ( reg[b] != 0 ) {
    std::vector<uint32_t>* prog = mem[reg[b]];
    auto copy = new std::vector<uint32_t>( *prog );
    delete mem[0];
    mem[0] = copy;
  }
  i = reg[c]-1;
  return;
}

void UM::orthography(uint32_t a, uint32_t v) {
  reg[a] = v;
  return;
}

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
    uint32_t a,b,c,v;
    if (op==13) {
      a = p >> (32-4-3) & 0b111;
      v = p & 0b00000001111111111111111111111111;
      //std::cout << op << " " << a << " " << v << std::endl;
    } else {
      a = (p & 0b111000000) >> 6;
      b = (p & 0b000111000) >> 3;
      c = (p & 0b000000111) >> 0;
      //std::cout << op << " " << a << " " << b << " " << c << std::endl;         
    }

    switch(op) {
    case  0: conditional_move(a,b,c); break;
    case  1: array_index(a,b,c); break;
    case  2: array_amendment(a,b,c); break;
    case  3: addition(a,b,c); break;
    case  4: multiplication(a,b,c); break;
    case  5: division(a,b,c); break;
    case  6: not_and(a,b,c); break;
    case  7: halt(a,b,c); break;
    case  8: allocation(a,b,c); break;
    case  9: abandonement(a,b,c); break;
    case 10: output_(a,b,c); break;
    case 11: input_(a,b,c); break;
    case 12: load_program(a,b,c); break;
    case 13: orthography(a,v); break;
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
