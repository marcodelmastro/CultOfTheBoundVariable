#!/bin/zsh
cat trypasswords.ins | pypy3 ../um.py ../umz/dump.um - |& tee trypasswords.log
