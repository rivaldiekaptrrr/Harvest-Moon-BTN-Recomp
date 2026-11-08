import struct

with open('extracted/A_FILE.HDT', 'rb') as f:
    hdt = f.read()
entries = struct.unpack(f'<{len(hdt)//4}I', hdt)

table = {
    0x0FFD: ' ',
    0xFFFE: '\n',
    0xFFFF: '<END>',
    0x006C: '.',
    0x008C: ',',
    0x0062: '?',
    0x0060: '!',
    0x0069: '-',
    0x0050: "'t",
    0x0051: "'s",
    0x0054: "'m",
    0x007F: '<PAGE>',
}
for i in range(26):
    table[i] = chr(ord('A') + i)
for i in range(26):
    table[0x20 + i] = chr(ord('a') + i)
for i in range(10):
    table[0x40 + i] = chr(ord('0') + i)

with open('extracted/A_FILE.BIN', 'rb') as f:
    start = entries[29]
    size = entries[30] - start
    f.seek(start)
    data = f.read(size)
    words = struct.unpack(f'<{len(data)//2}H', data)
    print(f"MesEv.Bin has {len(words)} words ({size} bytes)")
    i = 0
    while i < len(words):
        if words[i] in table and table[words[i]].isupper():
            sent = []
            j = i
            while j < len(words) and words[j] != 0xFFFF:
                w = words[j]
                sent.append(table.get(w, f'<{w:04X}>'))
                j += 1
            text = ''.join(sent)
            if text.count(' ') >= 2 and sum(1 for c in text if c.isalpha()) >= 8:
                raw_hex = data[i*2:j*2].hex()
                print(f"+0x{i*2:04X}: {text}")
                print(f"  HEX: {raw_hex}\n")
                i = j
        i += 1

