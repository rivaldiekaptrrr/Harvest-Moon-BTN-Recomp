import struct
import re

with open('extracted/A_FILE.HDT', 'rb') as f:
    hdt = f.read()
entries = struct.unpack(f'<{len(hdt)//4}I', hdt)

# Subfile 27 = Obj\GF_TITLE.Bin
start = entries[27]
size = entries[28] - start
with open('extracted/A_FILE.BIN', 'rb') as f:
    f.seek(start)
    data = f.read(size)

print(f"GF_TITLE.Bin size: {len(data)}")
for m in re.finditer(b'[A-Za-z0-9 _-]{4,}', data):
    print("ASCII:", m.group().decode('latin1'))

table = {0x0FFD: ' ', 0xFFFE: '\n', 0xFFFF: '<END>'}
for i in range(26): table[i] = chr(ord('A') + i)
for i in range(26): table[0x20 + i] = chr(ord('a') + i)

words = struct.unpack(f'<{len(data)//2}H', data)
for i in range(len(words)-4):
    w = words[i:i+6]
    if all(x in table and table[x].isalpha() for x in w):
        text = ''.join(table[x] for x in w)
        print(f"HM 16-bit at 0x{i*2:X}: {text}")

