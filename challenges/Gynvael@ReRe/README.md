# ReRe by Gynvael

## Intro

This crackme is from Gynvael's [Hacking Livestream #1: ReRe and EZPZP](https://www.youtube.com/watch?v=JExnV1-GNxk).

Archives:

* [confidence-teaser-2016-ds-gynvael-rere.zip](confidence-teaser-2016-ds-gynvael-rere.zip) - original archive with full source code and solution
* [rere.py.tar.gz](rere.py.tar.gz) - archive with the challenge only

## Solution

The ReRe crackme is a Python based script that constructs two functions - `_` and `crackme`, using raw bytecode blobs. When trying to disassemble the code objects by `dis.dis` you get junk and eventually the `dis.dis` crashes.

### Unpacking

Python internally compiles its programs into stack based bytecode. The instruction set is simple and the length of each instruction is 3 bytes - OPCODE, ARGUMENT and an EXTRA_ARGUMENT. This makes it pretty easy for analysis and understanding. The [dis](https://docs.python.org/2.7/library/dis.html) module is used to parse raw bytecode and get its meaning. The format of its output is described and there is also a good reference to all the opcodes and their arguments.

After an initial analysis it is obvious that there is a packer present. We have a `JUMP_ABSOLUTE` instruction then there is the stub body and at the end we have a control transferred back at offset 16. As part of another anti-re trick - a lot of `JUMP_FORWARD` instructions were used as part of dead code obfuscation. The original `dis.dis` function is not capable to properly handle this so I wrote a modified version of `dis` where I do very simple control flow checks to eliminate dead code listings - [dispy.py](https://github.com/mr6r4y/re-misc/blob/master/relib/dispy.py). I also changed the format of the output so I can easily process it:

```python
(ind, opn, op_arg, op_extarg, jmp_offset, desc)
```

Armed with this I could handle the `_` function and fully analyze it - [initial_analysis.md](work-notes/initial_analysis.md). The packing scheme is using the first 13 bytes after the `JUMP_ABSOLUTE` to `XOR` the packed code. The same packing mechanism is used for `crackme` function. With [disas_rere.py](disas_rere.py) I could play around and disassemble `_` which role is to encode strings:

```python
def _(x):
    return s[::-1].decode("zlib")
```

When trying to unpack and analyze `crackme` with the same approach, I hit another two obstacles:

* all strings in `crackme` were encoded with `_`
* it had another layer of packing using the same system

I had to automate the whole unpacking process. In order to do that and to assemble the function definitions in `crackme` I wrote a simple Python bytecode interpreter - `SimplePythonInterp` in [unpack_crackme.py](unpack_crackme.py). In `unpack_crackme.py` I automate the unpacking process and the decoding of the strings. `unpack_crackme.py` produces a fully unpacked bytecode disassembly of `crackme` - [rere_crackme_unpk.btc](work-notes/rere_crackme_unpk.btc).

### Searching for the Key

The analysis of ReRe on the fully unpacked Python bytecode in itself could be a standalone challenge. There were several obstacles to overcome:

* Flag check was spread into multiple functions
* Function names were obfuscated
* One of the checks obfuscated the `INPUT`(user input) and `VSYNC`(flag's flag) variable names (this check could be found only by the method of exclusion)

First I started with the `main`:

```python
InitGlobals()
ftime_base = time.time()
hashlib.md5('DrgnS{PythonRESoHard!}')  ## Troll!
InitGfx()
if WINNT:
    PaletteArchive()
ChangeCursor('show', False)
ChangeBuffering('on', False)
ChangeEcho('show', False)
while True:
  ch = MaybeGetChar()
  if ch is not None:
      o = ord(ch)
      if 32 <= o and o <= 126 and len(INPUT) < 26:
          INPUT += ch
  ftime = time.time() - ftime_base
  Gfx(ftime)
  time.sleep(0.01)
```

From `main` I knew that I have to follow `INPUT` all over the code and had to check `Gfx`. After a while I figured out the scheme and could convert the spread flag checks into:

```python
def check_key(INPUT):
    # InitGlobals
    VSYNC = True

    # PrepareFBForBlit
    f = [ord(x) for x in INPUT[7:21][::-2].ljust(7)]
    b = [110, 31, 97, 99, 101, 74, 105, 34, 101, 99, 65, 102, 67][::2]
    VSYNC = not any([f_idx ^ b_idx for f_idx, b_idx in zip(f, b)]) and VSYNC

    # LoadFont
    font_name = 'Sans Serif Monospace'
    VSYNC = not ord(INPUT[6:7].ljust(1)) ^ ord(font_name[5]) and VSYNC

    # FinalizeFrameBuffer
    f = f = [ord(i) for i in INPUT[7:22][::-2].ljust(8)]
    b = [98, 105, 82, 107, 76, 114, 115, 77]
    VSYNC = not any([f_idx ^ b_idx for f_idx, b_idx in zip(f, b)]) and VSYNC

    # ResetConsole
    vsync_options = [ord(i) ^ 153 for i in INPUT[22:].ljust(4)]
    vsync_options = vsync_options[3] << 24 | vsync_options[2] << 16 | (vsync_options[1] << 8) | vsync_options[0]
    VSYNC = not bool(vsync_options ^ 0xe4eaeef6) and VSYNC

    return VSYNC
```

By reversing the checks:

```python
def keygen():
    k = ["x"] * 26
    for i, j in zip(range(7, 21)[::-2], [110, 31, 97, 99, 101, 74, 105, 34, 101, 99, 65, 102, 67][::2]):
        k[i] = chr(j)
    k[6] = 'Sans Serif Monospace'[5]
    for i, j in zip(range(7, 22)[::-2], [98, 105, 82, 107, 76, 114, 115, 77]):
        k[i] = chr(j)
    for i, j in zip(range(22, 26), [((0xe4eaeef6 >> 8*i) & 0xff) ^ 153 for i in range(4)]):
        k[i] = chr(j)

    return "".join(k)
```

I figured out the flag structure to:

    xxxxxxSMCsAreLikeRainbows}

Then I actually guessed the right flag based on the known format used by Gynvael - `DrgnS{...}`:

    DrgnS{SMCsAreLikeRainbows}

Now what I had to do is to find the check and confirm. That appeared to be the most difficult task of the second part of the challenge. By the method of exclusion I ended up with `CheckPaletteSync` as the biggest suspect. The trick there is that there are no obvious references to `INPUT` and `VSYNC` variables. They are encoded in a list and `zlib` string decoding is used to get the names. The variable reference is obtained by `globals()[..]`:

```python
# CheckPaletteSync
# -------------------
palette_ordinals = [76, 35, 169, 224, 138, 152, 68, 95, 114, 203, 29, 210, 123, 29, 162, 56, 120, 156, 243, 244, 11, 8, 13, 1, 0, 4, 152, 1, 145, 120, 156, 11, 11, 142, 244, 115, 6,
pal = globals()[''.join([chr(i) for i in palette_ordinals][16:29]).decode("colorzlib"[5:])] # INPUT

#  MD5 of the first 6 chars from the input are checked against 4c23a9e08a98445f72cb1dd27b1da238
pal = [ord(i) for i in hashlib.md5(pal[:6]).digest()]
sync = [screen_ord ^ pal_ord for screen_ord, pal_ord in zip(pal, palette_ordinals[:16])]

# ANDed with VSYNC
pal_index = globals()[''.join([chr(i) for i in palette_ordinals][29:]).decode("colorzlib"[5:])] # VSYNC
globals()['VSYNC'] = int(not any(sync)) & globals()['VSYNC']
```

A simple hash check on the internet shows that: `md5('DrgnS{') == '4c23a9e08a98445f72cb1dd27b1da238'` and that is the last piece of the puzzle.
