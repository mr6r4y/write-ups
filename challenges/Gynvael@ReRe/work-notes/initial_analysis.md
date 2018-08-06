
## Function: _

```
(0, 'JUMP_ABSOLUTE', 266, 0, 266, '(to 266)')
(272, 'LOAD_GLOBAL', 3, 0, None, '(getattr)')
(281, 'LOAD_GLOBAL', 4, 0, None, '(_)')
(284, 'LOAD_CONST', 13, 0, None, "('e')")
(293, 'LOAD_GLOBAL', 5, 0, None, '(True)')
(296, 'CALL_FUNCTION', 3, 0, None, None)
(299, 'STORE_FAST', 2, 0, None, '(state)')

(302, 'LOAD_GLOBAL', 4, 0, None, '(_)')
(305, 'LOAD_ATTR', 6, 0, None, '(func_code)')
(315, 'LOAD_ATTR', 7, 0, None, '(co_code)')
(322, 'STORE_FAST', 3, 0, None, '(c)')

(332, 'LOAD_GLOBAL', 8, 0, None, '(getsizeof)')
(339, 'LOAD_CONST', 14, 0, None, "('')")
(352, 'CALL_FUNCTION', 1, 0, None, None)
(355, 'LOAD_CONST', 15, 0, None, '(1)')
(358, 'BINARY_SUBTRACT', None, None, None, None)
(359, 'STORE_FAST', 4, 0, None, '(off)')

(370, 'LOAD_GLOBAL', 9, 0, None, '(c_byte)')
(373, 'LOAD_GLOBAL', 10, 0, None, '(len)')
(387, 'LOAD_FAST', 3, 0, None, '(c)')
(402, 'CALL_FUNCTION', 1, 0, None, None)
(410, 'BINARY_MULTIPLY', None, None, None, None)
(411, 'LOAD_ATTR', 11, 0, None, '(from_address)')
(414, 'LOAD_GLOBAL', 12, 0, None, '(id)')
(423, 'LOAD_FAST', 3, 0, None, '(c)')
(430, 'CALL_FUNCTION', 1, 0, None, None)
(444, 'LOAD_FAST', 4, 0, None, '(off)')
(455, 'BINARY_ADD', None, None, None, None)
(466, 'CALL_FUNCTION', 1, 0, None, None)
(474, 'STORE_FAST', 5, 0, None, '(ptr)')

(482, 'LOAD_GLOBAL', 13, 0, None, '(map)')
(485, 'LOAD_GLOBAL', 14, 0, None, '(ord)')
(497, 'LOAD_FAST', 3, 0, None, '(c)')
(505, 'LOAD_CONST', 16, 0, None, '(3)')
(513, 'LOAD_CONST', 17, 0, None, '(16)')
(516, 'SLICE+3', None, None, None, None)
(517, 'CALL_FUNCTION', 2, 0, None, None)
(527, 'STORE_FAST', 6, 0, None, '(key)')

(530, 'LOAD_CONST', 18, 0, None, '(250)')
(533, 'STORE_FAST', 7, 0, None, '(sz)')

(536, 'LOAD_CONST', 19, 0, None, '(0)')
(549, 'STORE_FAST', 8, 0, None, '(i)')

(558, 'SETUP_LOOP', 169, 0, 730, '(to 730)')


(561, 'LOAD_FAST', 8, 0, None, '(i)')
(569, 'LOAD_FAST', 7, 0, None, '(sz)')
(579, 'COMPARE_OP', 0, 0, None, '(<)')

(593, 'POP_JUMP_IF_FALSE', 721, 0, 721, '(to 721)')

(596, 'LOAD_FAST', 5, 0, None, '(ptr)')

(607, 'LOAD_CONST', 21, 0, None, '(16)')
(610, 'LOAD_FAST', 8, 0, None, '(i)')
(623, 'BINARY_ADD', None, None, None, None)

(634, 'DUP_TOPX', 2, 0, None, None)
(649, 'BINARY_SUBSCR', None, None, None, None)

(650, 'LOAD_FAST', 6, 0, None, '(key)')

(663, 'LOAD_FAST', 8, 0, None, '(i)')
(676, 'LOAD_CONST', 20, 0, None, '(13)')
(679, 'BINARY_MODULO', None, None, None, None)
(686, 'BINARY_SUBSCR', None, None, None, None)

(692, 'INPLACE_XOR', None, None, None, None)

(693, 'ROT_THREE', None, None, None, None)
(694, 'STORE_SUBSCR', None, None, None, None)

(699, 'LOAD_FAST', 8, 0, None, '(i)')
(702, 'LOAD_CONST', 15, 0, None, '(1)')
(705, 'INPLACE_ADD', None, None, None, None)
(706, 'STORE_FAST', 8, 0, None, '(i)')

(718, 'JUMP_ABSOLUTE', 561, 0, 561, '(to 561)')


(721, 'POP_BLOCK', None, None, None, None)


(730, 'LOAD_FAST', 2, 0, None, '(state)')
(733, 'POP_JUMP_IF_TRUE', 799, 0, 799, '(to 799)')

(736, 'LOAD_GLOBAL', 15, 0, None, '(setattr)')
(739, 'LOAD_GLOBAL', 4, 0, None, '(_)')
(750, 'LOAD_CONST', 13, 0, None, "('e')")
(753, 'LOAD_GLOBAL', 5, 0, None, '(True)')
(760, 'CALL_FUNCTION', 3, 0, None, None)
(774, 'POP_TOP', None, None, None, None)
(775, 'NOP', None, None, None, None)
(786, 'NOP', None, None, None, None)
(797, 'NOP', None, None, None, None)
(798, 'RETURN_VALUE', None, None, None, None)

(799, 'LOAD_GLOBAL', 15, 0, None, '(setattr)')
(802, 'LOAD_GLOBAL', 4, 0, None, '(_)')
(812, 'LOAD_CONST', 13, 0, None, "('e')")
(820, 'LOAD_GLOBAL', 16, 0, None, '(False)')
(831, 'CALL_FUNCTION', 3, 0, None, None)
(834, 'POP_TOP', None, None, None, None)
(840, 'LOAD_CONST', 12, 0, None, '(None)')
(843, 'JUMP_ABSOLUTE', 16, 0, 16, '(to 16)')

```

```python
state = getattr(_, 'e', True)
c = _.func_code.co_code
off = getsizeof('') - 1
ptr = (c_byte * len(c)).from_address(id(c) + off)
key = map(ord, c[3:16])

sz = 250
i = 0
while i < sz:
    ptr[i + 16] ^= key[(i % 13)]
    i += 1

if not state:
    state = getattr(_, 'e', True)
    return 
else:
    setattr(_, 'e', False)
    # Execute payload:
    # (843, 'JUMP_ABSOLUTE', 16, 0, 16, '(to 16)')
    
```

# Function: _ (payload)

```
(16, 'LOAD_FAST', 0, 0, None, '(s)')

(19, 'LOAD_CONST', 0, 0, None, '(None)')
(22, 'LOAD_CONST', 0, 0, None, '(None)')
(30, 'LOAD_CONST', 1, 0, None, '(-1)')
(38, 'BUILD_SLICE', 3, 0, None, None)

(47, 'BINARY_SUBSCR', None, None, None, None)

(48, 'LOAD_ATTR', 0, 0, None, '(decode)')

(55, 'LOAD_CONST', 2, 0, None, "('')")
(58, 'LOAD_ATTR', 1, 0, None, '(join)')
(61, 'BUILD_LIST', 0, 0, None, None)
(71, 'LOAD_CONST', 3, 0, None, '(99)')
(84, 'LOAD_CONST', 4, 0, None, '(98)')
(87, 'LOAD_CONST', 5, 0, None, '(102)')
(90, 'LOAD_CONST', 6, 0, None, '(105)')
(93, 'LOAD_CONST', 7, 0, None, '(104)')
(104, 'LOAD_CONST', 8, 0, None, '(108)')
(107, 'LOAD_CONST', 9, 0, None, '(111)')
(110, 'LOAD_CONST', 10, 0, None, '(122)')
(113, 'BUILD_LIST', 8, 0, None, None)
(123, 'LOAD_CONST', 0, 0, None, '(None)')
(126, 'LOAD_CONST', 0, 0, None, '(None)')
(136, 'LOAD_CONST', 11, 0, None, '(-2)')
(150, 'BUILD_SLICE', 3, 0, None, None)
(165, 'BINARY_SUBSCR', None, None, None, None)
(178, 'GET_ITER', None, None, None, None)
(186, 'FOR_ITER', 63, 0, 252, '(to 252)')
(201, 'STORE_FAST', 1, 0, None, '(x)')
(211, 'LOAD_GLOBAL', 2, 0, None, '(chr)')
(214, 'LOAD_FAST', 1, 0, None, '(x)')
(217, 'CALL_FUNCTION', 1, 0, None, None)
(230, 'LIST_APPEND', 2, 0, None, None)
(237, 'JUMP_ABSOLUTE', 186, 0, 186, '(to 186)')
```

```python
return s[::-1].decode("".join([chr(i) for i in [99, 98, 102, 105, 104, 108, 111, 122]])[::-2])
=>
return s[::-1].decode("zlib")
```

# Function: crackme

```
(0, 'JUMP_ABSOLUTE', 44649, 0, 44649, '(to 44649)')
(44665, 'LOAD_GLOBAL', 37, 0, None, '(getattr)')
(44672, 'LOAD_GLOBAL', 38, 0, None, '(crackme)')
(44675, 'LOAD_CONST', 634, 0, None, "('e')")
(44685, 'LOAD_GLOBAL', 39, 0, None, '(True)')
(44700, 'CALL_FUNCTION', 3, 0, None, None)
(44703, 'STORE_FAST', 0, 0, None, '(state)')

(44706, 'LOAD_GLOBAL', 38, 0, None, '(crackme)')
(44709, 'LOAD_ATTR', 40, 0, None, '(func_code)')
(44712, 'LOAD_ATTR', 41, 0, None, '(co_code)')
(44715, 'STORE_FAST', 1, 0, None, '(c)')

(44726, 'LOAD_GLOBAL', 42, 0, None, '(getsizeof)')
(44729, 'LOAD_CONST', 635, 0, None, "('')")
(44737, 'CALL_FUNCTION', 1, 0, None, None)
(44748, 'LOAD_CONST', 636, 0, None, '(1)')
(44760, 'BINARY_SUBTRACT', None, None, None, None)
(44768, 'STORE_FAST', 2, 0, None, '(off)')

(44782, 'LOAD_GLOBAL', 43, 0, None, '(c_byte)')
(44792, 'LOAD_GLOBAL', 44, 0, None, '(len)')
(44795, 'LOAD_FAST', 1, 0, None, '(c)')
(44798, 'CALL_FUNCTION', 1, 0, None, None)
(44801, 'BINARY_MULTIPLY', None, None, None, None)
(44802, 'LOAD_ATTR', 45, 0, None, '(from_address)')
(44805, 'LOAD_GLOBAL', 46, 0, None, '(id)')
(44819, 'LOAD_FAST', 1, 0, None, '(c)')
(44831, 'CALL_FUNCTION', 1, 0, None, None)
(44834, 'LOAD_FAST', 2, 0, None, '(off)')
(44845, 'BINARY_ADD', None, None, None, None)
(44846, 'CALL_FUNCTION', 1, 0, None, None)
(44849, 'STORE_FAST', 3, 0, None, '(ptr)')

(44862, 'LOAD_GLOBAL', 47, 0, None, '(map)')
(44874, 'LOAD_GLOBAL', 48, 0, None, '(ord)')
(44887, 'LOAD_FAST', 1, 0, None, '(c)')
(44897, 'LOAD_CONST', 637, 0, None, '(3)')
(44906, 'LOAD_CONST', 638, 0, None, '(16)')
(44914, 'SLICE+3', None, None, None, None)
(44915, 'CALL_FUNCTION', 2, 0, None, None)
(44918, 'STORE_FAST', 4, 0, None, '(key)')

(44927, 'LOAD_CONST', 639, 0, None, '(44633)')
(44930, 'STORE_FAST', 5, 0, None, '(sz)')

(44933, 'LOAD_CONST', 640, 0, None, '(0)')
(44936, 'STORE_FAST', 6, 0, None, '(i)')

(44950, 'SETUP_LOOP', 147, 0, 45100, '(to 45100)')
(44965, 'LOAD_FAST', 6, 0, None, '(i)')
(44968, 'LOAD_FAST', 5, 0, None, '(sz)')
(44971, 'COMPARE_OP', 0, 0, None, '(<)')
(44974, 'POP_JUMP_IF_FALSE', 45087, 0, 45087, '(to 45087)')
(44989, 'LOAD_FAST', 3, 0, None, '(ptr)')
(44992, 'LOAD_CONST', 642, 0, None, '(16)')
(44995, 'LOAD_FAST', 6, 0, None, '(i)')
(45003, 'BINARY_ADD', None, None, None, None)
(45014, 'DUP_TOPX', 2, 0, None, None)
(45017, 'BINARY_SUBSCR', None, None, None, None)
(45018, 'LOAD_FAST', 4, 0, None, '(key)')
(45028, 'LOAD_FAST', 6, 0, None, '(i)')
(45031, 'LOAD_CONST', 641, 0, None, '(13)')
(45038, 'BINARY_MODULO', None, None, None, None)
(45039, 'BINARY_SUBSCR', None, None, None, None)
(45049, 'INPLACE_XOR', None, None, None, None)
(45050, 'ROT_THREE', None, None, None, None)
(45051, 'STORE_SUBSCR', None, None, None, None)
(45060, 'LOAD_FAST', 6, 0, None, '(i)')
(45068, 'LOAD_CONST', 636, 0, None, '(1)')
(45071, 'INPLACE_ADD', None, None, None, None)
(45072, 'STORE_FAST', 6, 0, None, '(i)')
(45075, 'JUMP_ABSOLUTE', 44965, 0, 44965, '(to 44965)')
(45087, 'POP_BLOCK', None, None, None, None)
(45100, 'LOAD_FAST', 0, 0, None, '(state)')

(45115, 'POP_JUMP_IF_TRUE', 45160, 0, 45160, '(to 45160)')

(45125, 'LOAD_GLOBAL', 49, 0, None, '(setattr)')
(45128, 'LOAD_GLOBAL', 38, 0, None, '(crackme)')
(45131, 'LOAD_CONST', 634, 0, None, "('e')")
(45134, 'LOAD_GLOBAL', 39, 0, None, '(True)')
(45137, 'CALL_FUNCTION', 3, 0, None, None)
(45150, 'POP_TOP', None, None, None, None)
(45151, 'NOP', None, None, None, None)
(45152, 'NOP', None, None, None, None)
(45153, 'NOP', None, None, None, None)
(45154, 'RETURN_VALUE', None, None, None, None)

(45160, 'LOAD_GLOBAL', 49, 0, None, '(setattr)')
(45171, 'LOAD_GLOBAL', 38, 0, None, '(crackme)')
(45184, 'LOAD_CONST', 634, 0, None, "('e')")
(45187, 'LOAD_GLOBAL', 50, 0, None, '(False)')
(45190, 'CALL_FUNCTION', 3, 0, None, None)
(45202, 'POP_TOP', None, None, None, None)
(45212, 'LOAD_CONST', 633, 0, None, '(None)')
(45215, 'JUMP_ABSOLUTE', 16, 0, 16, '(to 16)')
```

```python
state = getattr(crackme, 'e', True)
c = crackme.func_code.co_code
off = getsizeof('') - 1
ptr = (c_byte * len(c)).from_address(id(c) + off)
key = map(ord, c[3:16])

sz = 44633
i = 0
while i < sz:
    ptr[i + 16] ^= key[(i % 13)]
    i += 1

if not state:
    state = getattr(crackme, 'e', True)
    return 
else:
    setattr(crackme, 'e', False)
    # Execute payload:
    # (843, 'JUMP_ABSOLUTE', 16, 0, 16, '(to 16)')
```
