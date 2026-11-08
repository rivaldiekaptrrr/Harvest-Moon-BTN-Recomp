import struct

with open('extracted/A_FILE.HDT', 'rb') as f:
    hdt = f.read()
entries = struct.unpack(f'<{len(hdt)//4}I', hdt)

table = {
    0x0FFD: ' ', 0xFFFE: '\n', 0xFFFF: '<END>',
    0x006C: '.', 0x008C: ',', 0x0062: '?', 0x0060: '!',
    0x0069: '-', 0x0050: "'t", 0x0051: "'s", 0x0054: "'m",
    0x0055: "'ve", 0x0056: "'re", 0x0052: "'ll", 0x008E: '"',
    0x007F: '\f',
}
for i in range(26): table[i] = chr(ord('A') + i)
for i in range(26): table[0x20 + i] = chr(ord('a') + i)
for i in range(10): table[0x40 + i] = chr(ord('0') + i)

with open('extracted/A_FILE.BIN', 'rb') as f:
    start = entries[5]
    f.seek(start + 0x745800)
    data = f.read(0x800)
    words = struct.unpack(f'<{len(data)//2}H', data)
    text = ''.join(table.get(w, f'<{w:04X}>') for w in words)
    print("Decoded text at +0x745800:")
    print(text)
    print("\nRaw Hex:")
    print(data.hex())
