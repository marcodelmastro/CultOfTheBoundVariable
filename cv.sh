#!/bin/zsh
cat cv.ins publications.txt| ./um ./umz/dump.um |& tee cv.log
