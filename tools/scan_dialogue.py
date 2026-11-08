import struct
import re

with open('extracted/A_FILE.HDT', 'rb') as f:
    hdt = f.read()
entries = struct.unpack(f'<{len(hdt)//4}I', hdt)

keywords = ['farm', 'dog', 'cow', 'horse', 'mayor', 'mineral', 'turnip', 'potato', 
            'water', 'seed', 'tool', 'rucksack', 'harvest', 'festival', 'chicken', 
            'egg', 'milk', 'ranch', 'field', 'flower', 'season', 'spring', 'summer', 
            'fall', 'winter', 'good morning', 'hello', 'thank', 'welcome', 'money']

with open('extracted/A_FILE.BIN', 'rb') as f:
    for i in range(len(entries) - 1):
        start = entries[i]
        length = entries[i+1] - start
        f.seek(start)
        data = f.read(length)
        matches = re.findall(b'[\x20-\x7E]{5,}', data)
        readable = [m.decode('latin1', errors='ignore').strip() for m in matches if len(m.strip()) >= 5]
        dialogue = [s for s in readable if any(w in s.lower() for w in keywords)]
        print(f"Subfile {i:02d} ({length//1024:5d} KB): {len(readable):4d} text strings, {len(dialogue):3d} game keywords")
        if dialogue:
            print("   Samples:")
            for s in dialogue[:6]:
                print(f"     * {repr(s)}")

