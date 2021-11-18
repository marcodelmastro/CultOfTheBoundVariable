#!/usr/bin/env python

import sys, getopt
import struct
import os
import pickle

class UM:

    def readProg(self,infile="umz/sandmark.umz"):
        '''Load program from UMZ file'''
        program = []
        with open(infile, mode='rb') as file:
            part = file.read(4)
            while part:
                program.append(struct.unpack('>L', part)[0])                
                part = file.read(4)
            return program
    
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
        self.reg[a] = (self.reg[b]+self.reg[c]) & 0xFFFFFFFF
        return 

    def multiplication(self,a,b,c):
        # 4. Multiplication.
        # The register A receives the value in register B times
        # the value in register C, modulo 2^32.
        self.reg[a] = (self.reg[b]*self.reg[c]) & 0xFFFFFFFF
        return

    def division(self,a,b,c):
        # 5. Division.
        # The register A receives the value in register B
        # divided by the value in register C, if any, where
        # each quantity is treated as an unsigned 32 bit number.
        if self.reg[c]!=0:
            self.reg[a] = (self.reg[b] // self.reg[c]) & 0xFFFFFFFF
        return

    def not_and(self,a,b,c):
        # 6. Not-And.
        # Each bit in the register A receives the 1 bit if
        # either register B or register C has a 0 bit in that
        # position.  Otherwise the bit in register A receives
        # the 0 bit.~
        #self.reg[a] = (~self.reg[b] | ~self.reg[c]) & 0xFFFFFFFF
        self.reg[a] = (~(self.reg[b] & self.reg[c])) & 0xFFFFFFFF
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
        if len(self.freed)==0: # no free address, add a new one
            self.mem.append( [0] * self.reg[c] )
            self.reg[b] = len(self.mem)-1
        else: # use first available free address
            freeadd = self.freed.pop(0) 
            self.mem[freeadd] = [0] * self.reg[c]
            self.reg[b] = freeadd
        return

    def abandonement(self,a,b,c):
        # 9. Abandonment.
        # The array identified by the register C is abandoned.
        # Future allocations may then reuse that identifier.
        # **** NEED TO BOOKKEEP the FREED ADDRESSES! ****
        if 0<=self.reg[c]<len(self.mem):
            #self.mem[self.reg[c]] = []
            self.mem[self.reg[c]] = None
            self.freed.append(self.reg[c]) # keep a list of freed addresses
        else:
            self.status = -1
            print(" ** Abandonment FAIL **")
        return      

    def output_(self,a,b,c):
        # 10. Output.
        # The value in the register C is displayed on the console
        # immediately. Only values between and including 0 and 255
        # are allowed.
        if 0<=self.reg[c]<256:
            #print(chr(self.reg[c]),end="")
            sys.stdout.write(chr(self.reg[c]))
            sys.stdout.flush()
            if self.dump:
                cb = self.reg[c].to_bytes(1, byteorder='big')
                self.fd.write(cb)
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

        # buffer input command
        if not len(self.input):
            self.input = [ t for t in input()+"\n" ]
            # save status before exit
            if "".join(self.input[:-1])=="exit":
                with open(self.savfileout, "wb") as f:
                    print("Saving UM status in "+self.savfileout)
                    pickle.dump(self.mem,f)
                    pickle.dump(self.reg,f)
                    pickle.dump(self.freed,f)
                    pickle.dump(self.i,f)

        _c = self.input.pop(0)
        try:
            #_c = sys.stdin.read(1)
            self.reg[c] = ord(_c)
        except EOFError:
            self.input = []
            self.reg[c] = 0xFFFFFFFF
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
    
    def orthography(self,a,v):
        # 13. Orthography.
        # The value indicated is loaded into the register A
        # forthwith.
        self.reg[a] = v

    operation = [
            conditional_move,
            array_index,
            array_amendment,
            addition,
            multiplication,
            division,
            not_and,
            halt,
            allocation,
            abandonement,
            output_,
            input_,
            load_program,
            orthography
    ]  
    
    def __init__(self,infile=""):
        # platter arrays. 0 array initialized with program
        self.mem = [[]]
        if infile != "":
            self.mem[0] = self.readProg(infile)
            
        # list of reusable addresses
        self.freed = []
            
        # registers
        self.reg = [0, 0, 0, 0, 0, 0, 0, 0]
            
        # instruction index ("finger")
        self.i = 0
        
        # status (0 = HALT, 1 = RUNNING, -1 = FAIL)
        self.status = 0

        # dump output bytes to file
        self.dump = False
        self.fd = None

        # save files
        self.savfilein  = "status.sav"
        self.savfileout = "status.sav"

        # input buffer
        self.input = []
          
    def run(self):

        if self.dump:
            self.fd = open('dump.out','wb')
        
        self.status = 1
        
        while self.status>0:
            
            # If at the beginning of a cycle, the execution finger does not indicate 
            # a platter that describes a valid instruction, then the machine may Fail.          
            if self.i >= len(self.mem[0]):
                print(" ** Reached end of program **")
                return
            
            # get instruction from program array
            p = self.mem[0][self.i]
            
            # Decode instruction
            op = p >> (32-4)
            if op==13:
                a = p >> (32-4-3) & 0b111
                v = p & 0b00000001111111111111111111111111
                UM.operation[op](self,a,v)
            else:
                a = (p & 0b111000000) >> 6
                b = (p & 0b000111000) >> 3
                c = (p & 0b000000111) >> 0
                UM.operation[op](self,a,b,c)

            self.i += 1


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: um.py <file.um(z)>")
        return 0

    infile = sys.argv[1] 
    #um = UM(infile)
    um = UM()
    
    if len(sys.argv) > 2:
        if "-d" in sys.argv:
            um.dump = True
        if "-i" in sys.argv:            
            um.savfilein = sys.argv[sys.argv.index("-i")+1]
        if "-o" in sys.argv:            
            um.savfileout = sys.argv[sys.argv.index("-o")+1]
        
    files = os.listdir('.')
    if um.savfilein in files:
        print("Welcome to the Cult of Bound Variable")
        ans = "N"
        if "-i" not in sys.argv:  
            ans = input("Do you want to start from status saved in "+um.savfilein+"? [y/n]")
        if ans[0]=="Y" or ans[0]=='y' or "-i" in sys.argv:
            with open(um.savfilein, "rb") as f:
                print("Loading state from",um.savfilein,"... ",end="")
                um.mem = pickle.load(f)
                um.reg = pickle.load(f)
                um.freed = pickle.load(f)
                um.i = pickle.load(f)
                print("loaded.")
        else:
            um.mem[0] = um.readProg(infile)
    else:
        um.mem[0] = um.readProg(infile)
    
    um.run()
    
    return 1
            
if __name__ == "__main__":
    sys.exit(main())
