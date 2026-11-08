import struct

with open('extracted/A_FILE.HDT', 'rb') as f:
    hdt = f.read()
entries = struct.unpack(f'<{len(hdt)//4}I', hdt)

table = {0x0FFD: ' ', 0xFFFE: '\n', 0xFFFF: '<END>', 0x006C: '.', 0x008C: ',', 0x0054: "'m", 0x008E: '"'}
for i in range(26): table[i] = chr(ord('A') + i)
for i in range(26): table[0x20 + i] = chr(ord('a') + i)

with open('extracted/A_FILE.BIN', 'rb') as f:
    start = entries[5]
    # At 0x74581e was 'Mineral Town'
    f.seek(start + 0x74581e - 64)
    data = f.read(512)
    words = struct.unpack(f'<{len(data)//2}H', data)
    
    # find where 0xFFFF is (end of message)
    end_idx = -1
    for i, w in enumerate(words):
        if w == 0xFFFF:
            end_idx = i
            break
    
    print(f"Message length in words: {end_idx}")
    print("Full decoded text:")
    print(''.join(table.get(w, f'<{w:04X}>') for w in words[:end_idx+1]))
    print("\nRaw bytes (hex):")
    raw_msg = struct.pack(f'<{end_idx}H', *words[:end_idx])
    print(raw_msg.hex())

