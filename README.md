# Cult Of The Bound Variable

http://www.boundvariable.org/task.shtml

## Universal Machine development

### Python

Using pypy to speedup execution:

```
pypy3 ./um.py ./umz/sandmark.umz | tee ./umz/sandmark-myoutput.txt
```

## Codex processing

Running the UM on codex.umz proposed to "dump UM data"

```
um.py umz/codex.umz
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

Trying to save dump with:

```
cat umz/codex.ins | pypy3 um.py umz/codex.umz - > umz/dump.out
```

It took me a while to understand why this was not working! I'm using Python 3, so `sys.stdout.write(chr(self.reg[c]))` or `print(chr(self.reg[c]),end="")` are not outputting bytes to stout as in Python 2, but something that depends on the terminal encoding. I can probably leave the terminal output as it is, but add an option to dump the output as bytes to a file:

```
cat umz/codex.ins | pypy3 um.py umz/codex.umz -d
```

And it works!

## UMIX

Let the fun begin...

```
pypy3 um.py umz/dump.um
```

```
12:00:00 1/1/19100
Welcome to Universal Machine IX (UMIX).

This machine is a shared resource. Please do not log
in to multiple simultaneous UMIX servers. No game playing
is allowed.

Please log in (use 'guest' for visitor access).
;login:
```

### C++

After some digging of the UMIX system, I realised my python implementation is too slow to allow efficient attempts to solve of the various puzzles (for instance, the `adventure` game takes forever to load, it is thus impossible to automatize the searach for a correct sequence of actions). Therefore I am now trying to develop a `um` machine in C++. 

To compile:

```
make
```

To run the bentchmark tests:

```
./um ./umz/sandmark.umz
```

### Bentchmark

| Python (PyPY) | ``  |
| C++ | `2713.64s user 16.22s system 99% cpu 45:56.45 total`  |

