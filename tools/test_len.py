import struct

def encode_hm_string(s):
    out = bytearray()
    i = 0
    while i < len(s):
        if s[i] == '<' and i + 5 < len(s) and s[i+5] == '>':
            val = int(s[i+1:i+5], 16)
            out.extend(struct.pack('<H', val))
            i += 6
            continue
        c = s[i]
        if 'A' <= c <= 'Z':
            w = ord(c) - ord('A')
        elif 'a' <= c <= 'z':
            w = 0x20 + (ord(c) - ord('a'))
        elif '0' <= c <= '9':
            w = 0x40 + (ord(c) - ord('0'))
        elif c == ' ':
            w = 0x0FFD
        elif c == '\n':
            w = 0xFFFE
        elif c == '\f':
            w = 0x007F
        elif c == '.':
            w = 0x006C
        elif c == ',':
            w = 0x008C
        elif c == '?':
            w = 0x0062
        elif c == '!':
            w = 0x0060
        elif c == '-':
            w = 0x0069
        elif c == "'":
            w = 0x0051
        elif c == '"':
            w = 0x008E
        else:
            w = 0x0FFD
        out.extend(struct.pack('<H', w))
        i += 1
    return out

# Original English:
en = '<0F87><0FF7><0FF4>Welcome to "Mineral Town."\nI\'m Mayor Thomas.<0FFC><0FFB>\n<0F87><0FF7><0FF4>I\'m going to ask you a number\nof questions, so please answer\nthem.'
en_bytes = encode_hm_string(en)
print(f"EN len: {len(en_bytes)} bytes")

# Indonesian options:
options = [
    '<0F87><0FF7><0FF4>Selamat datang di "Mineral Town."\nSaya Walikota Thomas.<0FFC><0FFB>\n<0F87><0FF7><0FF4>Saya ingin bertanya beberapa\nhal, tolong dijawab ya.',
    '<0F87><0FF7><0FF4>Selamat datang di "Mineral Town."\nSaya Walikota Thomas.<0FFC><0FFB>\n<0F87><0FF7><0FF4>Saya akan mengajukan beberapa\npertanyaan, tolong dijawab ya.',
    '<0F87><0FF7><0FF4>Selamat datang di "Mineral Town."\nSaya Walikota Thomas.<0FFC><0FFB>\n<0F87><0FF7><0FF4>Saya ingin menanyakan beberapa\nhal, jadi tolong dijawab ya.',
]

for idx, opt in enumerate(options):
    enc = encode_hm_string(opt)
    print(f"Option {idx+1}: {len(enc)} bytes (Original was 234 bytes)")

