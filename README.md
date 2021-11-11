# Cult Of The Bound Variable

http://www.boundvariable.org/task.shtml

## Universal Machine development

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

```
pypy3 um.py umz/dump.um
```
