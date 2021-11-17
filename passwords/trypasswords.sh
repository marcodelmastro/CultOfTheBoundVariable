#!/bin/zsh

#cat trypasswords.ins | pypy3 ../um.py ../umz/dump.um - | tee trypasswords.log
cat trypasswords.ins | ../um ../umz/dump.um
