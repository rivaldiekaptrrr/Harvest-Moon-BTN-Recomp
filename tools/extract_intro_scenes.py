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
    size = entries[6] - start
    f.seek(start)
    data = f.read(min(size, 8000000))
    words = struct.unpack(f'<{len(data)//2}H', data)

    i = 0
    while i < len(words):
        if words[i] == 0xFFFF or words[i] == 0x0000:
            i += 1
            continue
        j = i
        while j < len(words) and words[j] != 0xFFFF:
            j += 1
        raw_words = words[i:j]
        letters = sum(1 for w in raw_words if w <= 0x0019 or (0x0020 <= w <= 0x0039) or w == 0x0FFD)
        if letters >= 15 and letters * 2 >= len(raw_words):
            raw_bytes = struct.pack(f'<{len(raw_words)}H', *raw_words)
            text = ''.join(table.get(w, f'<{w:04X}>') for w in raw_words)
            low_text = text.lower()
            if any(k in low_text for k in ['grandfather', 'mayor', 'thomas', 'mineral town', 'farm', 'years', 'dog', 'puppy', 'three years', 'ranch']):
                print(f"Offset +0x{i*2:06X}:")
                print(f"TEXT:\n{text.strip()}")
                print(f"HEX:\n{raw_bytes.hex()}\n")
        i = j + 1

