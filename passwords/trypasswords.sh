#!/bin/zsh
for user in ftd knr gardener ohmega yang howie hmonk bbarker
do
    echo Hacking user $user
    rm -f trypasswords_$user.ins
    cp -f trypasswords.ins trypasswords_$user.ins
    echo ./hackfix.exe $user >> trypasswords_$user.ins
    echo exit >> trypasswords_$user.ins
    cat trypasswords_$user.ins | pypy3 ../um.py ../umz/dump.um - | tee pass_${user}.log
    rm -f trypasswords_$user.ins
done
