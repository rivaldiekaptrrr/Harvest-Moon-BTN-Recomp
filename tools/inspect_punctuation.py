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
}
for i in range(26):
    table[i] = chr(ord('A') + i)
for i in range(26):
    table[0x20 + i] = chr(ord('a') + i)
for i in range(10):
    table[0x40 + i] = chr(ord('0') + i)

interesting_codes = [0x52, 0x53, 0x55, 0x56, 0x61, 0x63, 0x64, 0x65, 0x66, 0x68, 0x70, 0x71, 0x72, 0x77]

with open('extracted/A_FILE.BIN', 'rb') as f:
    for sub in [2, 3, 4, 5, 6]:
        start = entries[sub]
        f.seek(start)
        data = f.read(min(entries[sub+1] - start, 300000))
        words = struct.unpack(f'<{len(data)//2}H', data)
        for i, w in enumerate(words):
            if w in interesting_codes:
                # print snippet
                snippet = words[max(0, i-10):min(len(words), i+10)]
                dec = ''.join(table.get(x, f'<{x:02X}>') for x in snippet)
                print(f"Code 0x{w:02X} in: {dec}")
                if w in interesting_codes:
                    interesting_codes.remove(w)
                if not interesting_codes:
                    break
        if not interesting_codes:
            break

