import struct

with open('extracted/A_FILE.HDT', 'rb') as f:
    hdt = f.read()
entries = struct.unpack(f'<{len(hdt)//4}I', hdt)

with open('extracted/A_FILE.BIN', 'rb') as f:
    start = entries[5]
    f.seek(start + 0x745800)
    data = f.read(0x800)
    idx = data.find(b'\xff\xff')
    print("Offset of FFFF:", idx)
    zero_count = 0
    for b in data[idx+2:]:
        if b == 0:
            zero_count += 1
        else:
            break
    print("Zero padding bytes after FFFF:", zero_count)
