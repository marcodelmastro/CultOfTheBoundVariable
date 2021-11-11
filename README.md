# Cult Of The Bound Variable

http://www.boundvariable.org/task.shtml

## Universal Machine develpment

Using pypy to speedup execution:

```
pypy3 ./um.py ./umz/sandmark.umz | tee ./umz/sandmark-myoutput.txt
```

## Codex processing

Running the UM on codex.umz proposed to "dump UM data"

```
pypy3 um.py umz/codex.umz
```

```
self-check succeeded!
enter decryption key:
(\b.bb)(\v.vv)06FHPVboundvarHRAk
decrypting...
ok
LOADING: 9876543210

 == CBV ARCHIVE ==
    VOLUME ID 9

 Choose a command:

 p) dump UM data
 x) exit

?
```

Trying to save dump...

```
cat umz/codex.ins | pypy3 um.py umz/codex.umz - > umz/dump.out
```
