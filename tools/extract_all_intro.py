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
        if words[i] == 0xFFFF:
            i += 1
            continue
        # Scan for message start
        # A message starts either after padding 0 or at control codes 0x0Fxx or letters
        # Let's find end of message (0xFFFF)
        j = i
        letters = 0
        while j < len(words) and words[j] != 0xFFFF:
            w = words[j]
            if w <= 0x0019 or (0x0020 <= w <= 0x0039):
                letters += 1
            j += 1
        
        if letters >= 6 and j < len(words):
            # Trim leading zero padding
            k = i
            while k < j and words[k] == 0:
                k += 1
            raw_words = words[k:j]
            if raw_words:
                raw_bytes = struct.pack(f'<{len(raw_words)}H', *raw_words)
                text = ''.join(table.get(w, f'<{w:04X}>') for w in raw_words)
                # Check for interesting words
                if any(kw in text.lower() for kw in ['welcome', 'mineral town', 'thomas', 'grandfather', 'farm', 'three years', 'mayor', 'name', 'dog', 'puppy', 'spring', 'ranch']):
                    print(f"Offset +0x{k*2:06X}:")
                    print(f"  TEXT: {text.strip()}")
                    print(f"  HEX:  {raw_bytes.hex()}\n")
            i = j
        i += 1

