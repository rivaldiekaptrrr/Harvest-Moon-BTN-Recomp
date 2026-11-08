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
    0x0055: "'ve",
    0x0056: "'re",
    0x0052: "'ll",
    0x007F: '<PAGE>',
}
for i in range(26):
    table[i] = chr(ord('A') + i)
for i in range(26):
    table[0x20 + i] = chr(ord('a') + i)
for i in range(10):
    table[0x40 + i] = chr(ord('0') + i)

with open('extracted/A_FILE.BIN', 'rb') as f:
    for sub in [2, 3, 4, 5, 6]:
        start = entries[sub]
        size = entries[sub+1] - start
        f.seek(start)
        data = f.read(min(size, 400000))
        words = struct.unpack(f'<{len(data)//2}H', data)
        i = 0
        while i < len(words):
            if words[i] == 0xFFFF:
                i += 1
                continue
            if words[i] in table and table[words[i]].isupper():
                sent = []
                j = i
                while j < len(words) and words[j] != 0xFFFF:
                    w = words[j]
                    sent.append(table.get(w, f'<{w:04X}>'))
                    j += 1
                text = ''.join(sent)
                if any(w in text.lower() for w in ['mayor', 'thomas', 'grandfather', 'town', 'three years', 'dog', 'puppy', 'welcome', 'name']):
                    raw_words = words[i:j]
                    raw_hex = struct.pack(f'<{len(raw_words)}H', *raw_words).hex()
                    print(f"Sub {sub:02d} +0x{i*2:05X}:")
                    print(f"  EN: {text.strip()}")
                    print(f"  HEX: {raw_hex}")
                    print()
                    i = j
            i += 1

