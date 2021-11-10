#!/usr/bin/env python

import sys
import struct

class UM:
    
    def __init__(self,infile=""):
        # platter arrays. 0 array initialized with program
        self.mem = [[]]
        if infile != "":
            self.readProg(infile)
        
        # registers
        self.reg = [0, 0, 0, 0, 0, 0, 0, 0]
            
        # instruction index ("finger")
        self.i = 0

        # input buffer
        self.command = []
        
        # status (0 = HALT, 1 = RUNNING, -1 = FAIL)
        self.status = 0

        # max value
        self.m = 0b11111111111111111111111111111111
        
        # operator map
        self.operator = [
            self.conditional_move,
            self.array_index,
            self.array_amendment,
            self.addition,
            self.multiplication,
            self.division,
            self.not_and,
            self.halt,
            self.allocation,
            self.abandonement,
            self.output_,
            self.input_,
            self.load_program,
            self.orthography,
        ]    
        
    def readProg(self,infile="umz/sandmark.umz"):
        '''Load program from UMZ file'''
        with open(infile, mode='rb') as file:        
            part = file.read(4)
            while part:
                self.mem[0].append(struct.unpack('>L', part)[0])                
                part = file.read(4)

    def readProg2(self,infile):        
        with open(infile) as file:
            p = file.read(4)
            while len(p)==4:
                a = ord(p[0])
                b = ord(p[1])
                c = ord(p[2])
                d = ord(p[3])
                w = (a << 24) | (b << 16) | (c << 8) | (d)
                self.mem[0].append(w)
                p = file.read(4)
                
    def conditional_move(self,a,b,c):
        # 0. Conditional Move.
        # The register A receives the value in register B,
        # unless the register C contains 0.
        if self.reg[c] != 0: 
            self.reg[a] = self.reg[b]
        return

    def array_index(self,a,b,c):
        # 1. Array Index.
        # The register A receives the value stored at offset
        # in register C in the array identified by B.
        # ACTUALLY: identified by *value in register B!*
        #if self.reg[b]<len(self.mem):
        #    if self.reg[c]<len(self.mem[self.reg[b]]):
        self.reg[a] = self.mem[self.reg[b]][self.reg[c]]
        return

    def array_amendment(self,a,b,c):
        # 2. Array Amendment.
        # The array identified by A is amended at the offset
        # in register B to store the value in register C.
        # ACTUALLY: identified by *value in register A!*
        #if self.reg[a]<len(self.mem):
        #    if self.reg[b]<len(self.mem[self.reg[a]]):
        self.mem[self.reg[a]][self.reg[b]] = self.reg[c]
        return

    def addition(self,a,b,c):
        # 3. Addition.
        # The register A receives the value in register B plus 
        # the value in register C, modulo 2^32.
        self.reg[a] = (self.reg[b]+self.reg[c]) & self.m
        return 

    def multiplication(self,a,b,c):
        # 4. Multiplication.
        # The register A receives the value in register B times
        # the value in register C, modulo 2^32.
        self.reg[a] = (self.reg[b]*self.reg[c]) & self.m
        return

    def division(self,a,b,c):
        # 5. Division.
        # The register A receives the value in register B
        # divided by the value in register C, if any, where
        # each quantity is treated as an unsigned 32 bit number.
        if self.reg[c]>0:
            self.reg[a] = (self.reg[b] // self.reg[c])
        return

    def not_and(self,a,b,c):
        # 6. Not-And.
        # Each bit in the register A receives the 1 bit if
        # either register B or register C has a 0 bit in that
        # position.  Otherwise the bit in register A receives
        # the 0 bit.
        self.reg[a] = (~self.reg[b] & self.m) | (~self.reg[c] & self.m)
        return

    def halt(self,a,b,c):
        # 7. Halt.
        # The universal machine stops computation.
        self.status = 0
        return

    def allocation(self,a,b,c):
        # 8. Allocation.
        # A new array is created with a capacity of platters
        # commensurate to the value in the register C. This
        # new array is initialized entirely with platters
        # holding the value 0. A bit pattern not consisting of
        # exclusively the 0 bit, and that identifies no other
        # active allocated array, is placed in the B register.
        self.mem.append( [0] * self.reg[c] )
        self.reg[b] = len(self.mem)-1
        return

    def abandonement(self,a,b,c):
        # 9. Abandonment.
        # The array identified by the register C is abandoned.
        # Future allocations may then reuse that identifier.
        if self.reg[c]>0 and self.reg[c]<len(self.mem):
            self.mem[self.reg[c]] = []
        else:
            self.status = -1
            print(" ** Abandonment FAIL **")
        return      

    def output_(self,a,b,c):
        # 10. Output.
        # The value in the register C is displayed on the console
        # immediately. Only values between and including 0 and 255
        # are allowed.
        if self.reg[c]<=255:
            print(chr(self.reg[c]),end="")
        else:
            self.status = -1
            print(" ** Output FAIL **")
        return

    def input_(self,a,b,c):
        # 11. Input.
        # The universal machine waits for input on the console.
        # When input arrives, the register C is loaded with the
        # input, which must be between and including 0 and 255.
        # If the end of input has been signaled, then the 
        # register C is endowed with a uniform value pattern
        # where every place is pregnant with the 1 bit.
        if not len(self.command):
            self.command = list(input())
            self.i -= 1
            return
        else:
            while len(self.command):
                self.reg[c] = ord(self.command.pop(0)) #& 0xFF # avoid values larger than 255
                return
            self.reg[c] = self.m
            return

    def load_program(self,a,b,c):
        # 12. Load Program.
        # The array identified by the B register is duplicated
        # and the duplicate shall replace the '0' array,
        # regardless of size. The execution finger is placed
        # to indicate the platter of this array that is
        # described by the offset given in C, where the value
        # 0 denotes the first platter, 1 the second, et cetera.
        #
        # The '0' array shall be the most sublime choice for
        # loading, and shall be handled with the utmost
        # velocity.
        if self.reg[b] != 0: # do the copying only if needed!
            if len(self.mem[self.reg[b]]):
                self.mem[0] = list(self.mem[self.reg[b]])                
            else:
                self.status = -1
                print(" ** Load FAIL **")
        self.i = self.reg[c]-1 # subtract 1 since it'll be incremented later
        return
    
    def orthography(self,a,b,c):
        # 13. Orthography.
        # The value indicated is loaded into the register A
        # forthwith.
        self.reg[a] = b # replace v with b in call
                
    def run(self):
        
        a = 0
        b = 0
        c = 0
        v = 0     
        self.status = 1
        
        while self.status>0:
            
            # If at the beginning of a cycle, the execution finger does not indicate 
            # a platter that describes a valid instruction, then the machine may Fail.          
            if self.i > len(self.mem[0]):
                print(" ** Reached end of program **")
                return
            
            # get instruction from program array
            p = self.mem[0][self.i]
            
            # decode instruction
            op = p >> (32-4)
            if op==13:
                a = p >> (32-4-3) & 0b111
                v = p & 0b00000001111111111111111111111111
                self.operator[op](a,v,v)            
            else:
                a = (p & 0b111000000) >> 6
                b = (p & 0b000111000) >> 3
                c = (p & 0b000000111) >> 0
                self.operator[op](a,b,c)
            
            self.i += 1

#um = UM("umz/sandmark.umz")
um = UM(sys.argv[1])
um.run()
