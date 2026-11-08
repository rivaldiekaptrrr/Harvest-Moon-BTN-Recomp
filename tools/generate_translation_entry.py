import struct

def encode_hm_string(s):
    # HM 16-bit LE encoding
    out = bytearray()
    for c in s:
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
        else:
            w = 0x0FFD
        out.extend(struct.pack('<H', w))
    return out

test_phrases = [
    ("Supermarket", "Supermarket"),
    ("Saibara", "Saibara"),
    ("Farm", "Kebun"),
    ("stumps", "tunggul"),
    ("lumber", "kayu"),
    ("animals", "hewan"),
    ("careful", "hati-hati"),
    ("wisely", "dengan bijak"),
    ("Hi", "Halo"),
    ("What can I do for you?", "Ada yang bisa kubantu?"),
    ("Talk about part-time job.", "Bicara pekerjaan paruh waktu."),
    ("Don't talk about part-time job.", "Jangan bicara pekerjaan paruh waktu."),
]

print("# Generated translation entries for Harvest Moon: Back to Nature")
for en, id_text in test_phrases:
    hex_str = encode_hm_string(en).hex()
    print("[[entry]]")
    print(f'src_hex = "{hex_str}"')
    print(f'en = "{en}"')
    print(f'id = "{id_text}"')
    print('term = "ffff"\n')

