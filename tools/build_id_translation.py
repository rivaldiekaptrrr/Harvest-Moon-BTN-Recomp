import struct
import os

with open('extracted/A_FILE.HDT', 'rb') as f:
    hdt = f.read()
entries = struct.unpack(f'<{len(hdt)//4}I', hdt)

table = {
    0x0FFD: ' ', 0xFFFE: '\n', 0xFFFF: '',
    0x006C: '.', 0x008C: ',', 0x0062: '?', 0x0060: '!',
    0x0069: '-', 0x0050: "'t", 0x0051: "'s", 0x0054: "'m",
    0x0055: "'ve", 0x0056: "'re", 0x0052: "'ll", 0x008E: '"',
    0x007F: '\f',
}
for i in range(26): table[i] = chr(ord('A') + i)
for i in range(26): table[0x20 + i] = chr(ord('a') + i)
for i in range(10): table[0x40 + i] = chr(ord('0') + i)

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
        elif c == ':':
            w = 0x006C
        elif c == ';':
            w = 0x008C
        else:
            w = 0x0FFD
        out.extend(struct.pack('<H', w))
        i += 1
    return out

entries_toml = []

def add_entry(src_hex, en, id_text, term="ffff"):
    if not any(e["src_hex"] == src_hex for e in entries_toml):
        entries_toml.append({
            "src_hex": src_hex,
            "en": en,
            "id": id_text,
            "term": term
        })

# 1. Opening Dialogue with Mayor Thomas in Mineral Town
add_entry(
    "870ff70ff40f160024002b0022002e002c002400fd0f33002e00fd0f8e000c0028002d002400310020002b00fd0f13002e0036002d006c008e00feff08005400fd0f0c00200038002e003100fd0f130027002e002c00200032006c00fc0ffb0ffeff870ff70ff40f08005400fd0f26002e0028002d002600fd0f33002e00fd0f200032002a00fd0f38002e003400fd0f2000fd0f2d0034002c00210024003100feff2e002500fd0f3000340024003200330028002e002d0032008c00fd0f32002e00fd0f2f002b002400200032002400fd0f20002d003200360024003100feff3300270024002c006c00",
    '<0F87><0FF7><0FF4>Welcome to "Mineral Town."\nI\'m Mayor Thomas.<0FFC><0FFB>\n<0F87><0FF7><0FF4>I\'m going to ask you a number\nof questions, so please answer\nthem.',
    '<0F87><0FF7><0FF4>Selamat datang di "Mineral Town."\nSaya Walikota Thomas.<0FFC><0FFB>\n<0F87><0FF7><0FF4>Saya ingin bertanya beberapa\nhal, tolong dijawab ya.'
)

# 2. Name & Confirmation Questions
add_entry(
    "f30f08003200fd0f3300270028003200fd0f2d0020002c002400fd0f0e000a006200",
    "<0FF3>Is this name OK?",
    "<0FF3>Nama ini sudah benar?"
)
add_entry(
    "f30f08003200fd0f3300270028003200fd0f0e000a006200",
    "<0FF3>Is this OK?",
    "<0FF3>Apakah sudah benar?"
)
add_entry(
    "fa0ffefffd0f1300270028003200fd0f28003200fd0f0e000a00fefffd0f130031003800fd0f20002600200028002d00",
    "<0FFA>\n This is OK\n Try again",
    "<0FFA>\n Sudah benar\n Coba lagi"
)

# 3. System & UI Controls
add_entry(
    "f30f0300fd0f01003400330033002e002d006600fd0f0c002e0035002400fd0f02003400310032002e003100feff6e00fd0f01003400330033002e002d006600fd0f08002d002f0034003300feff6d00fd0f01003400330033002e002d006600fd0f0100200022002a00fd0ffeff12003300200031003300fd0ffd0ffd0f6600fd0f120024002b00240022003300fd0f0d0020002c002400fd0f",
    "<0FF3>D Button<0066> Move Cursor\n<006E> Button<0066> Input\n<006D> Button<0066> Back \nStart   <0066> Select Name ",
    "<0FF3>Tombol Arah<0066> Pindah Kursor\n<006E> Tombol<0066> Masukkan\n<006D> Tombol<0066> Kembali\nStart   <0066> Pilih Nama "
)
add_entry(
    "f30f0300fd0f21003400330033002e002d006600fd0f0c002e0035002400fd0f330027002400fd0f22003400310032002e003100feff6e00fd0f21003400330033002e002d006600fd0f120024002b00240022003300feff6d00fd0f21003400330033002e002d006600fd0f020020002d00220024002b00",
    "<0FF3>D button<0066> Move the cursor\n<006E> button<0066> Select\n<006D> button<0066> Cancel",
    "<0FF3>Tombol Arah<0066> Pindah kursor\n<006E> Tombol<0066> Pilih\n<006D> Tombol<0066> Batal"
)
add_entry(
    "f30f0300fd0f01003400330033002e002d006600fd0f0c002e0035002400fd0f02003400310032002e003100feff6e00fd0f01003400330033002e002d006600fd0f040037002f002b00200028002d00fd0f0000310024002000feff6d00fd0f01003400330033002e002d006600fd0f02002b002e0032002400feff12003300200031003300fd0ffd0ffd0f6600fd0f1500280024003600fd0f0500200031002c00",
    "<0FF3>D Button<0066> Move Cursor\n<006E> Button<0066> Explain Area\n<006D> Button<0066> Close\nStart   <0066> View Farm",
    "<0FF3>Tombol Arah<0066> Pindah Kursor\n<006E> Tombol<0066> Info Area\n<006D> Tombol<0066> Tutup\nStart   <0066> Lihat Kebun"
)
add_entry(
    "f30f0300fd0f21003400330033002e002d006600fd0f0c002e0035002400fd0f330027002400fd0f22003400310032002e003100feff6e00fd0f21003400330033002e002d006600fd0f120024002b00240022003300feff6d00fd0f21003400330033002e002d006600fd0f02002b002e0032002400fd0f360028002d0023002e003600",
    "<0FF3>D button<0066> Move the cursor\n<006E> button<0066> Select\n<006D> button<0066> Close window",
    "<0FF3>Tombol arah<0066> Pindah kursor\n<006E> tombol<0066> Pilih\n<006D> tombol<0066> Tutup jendela"
)
add_entry(
    "f30f0f00310024002f002000310028002d002600fd0f33002e00fd0f22002e002e002a006c00feff0f002b002400200032002400fd0f36002000280033006c00",
    "<0FF3>Preparing to cook.\nPlease wait.",
    "<0FF3>Bersiap memasak.\nMohon tunggu."
)
add_entry(
    "fa0ffefffd0f02002e002e002a00fd0f2300280032002700fefffd0f03002e00fd0f2d002e003300fd0f22002e002e002a00",
    "<0FFA>\n Cook dish\n Do not cook",
    "<0FFA>\n Masak hidangan\n Jangan masak"
)

# 4. Standard in-game lexicon
dictionary = {
    "Yes": "Ya",
    "No": "Tidak",
    "Talk": "Bicara",
    "Check": "Periksa",
    "Eat": "Makan",
    "Throw": "Lempar",
    "Put away": "Simpan",
    "Take out": "Keluarkan",
    "Farm": "Kebun",
    "Supermarket": "Supermarket",
    "Saibara": "Saibara",
    "stumps": "tunggul kayu",
    "lumber": "kayu",
    "animals": "hewan-hewan",
    "careful": "hati-hati",
    "wisely": "dengan bijak",
    "Hi": "Halo",
    "Hello": "Halo",
    "Good morning": "Selamat pagi",
    "Good afternoon": "Selamat siang",
    "Good evening": "Selamat malam",
    "Thank you": "Terima kasih",
    "Thanks": "Makasih",
    "Welcome": "Selamat datang",
    "What can I do for you?": "Ada yang bisa kubantu?",
    "Talk about part-time job.": "Bicara pekerjaan paruh waktu.",
    "Don't talk about part-time job.": "Jangan bicara pekerjaan paruh waktu.",
    "Spring": "Musim Semi",
    "Summer": "Musim Panas",
    "Fall": "Musim Gugur",
    "Winter": "Musim Dingin",
    "Turnip": "Lobak",
    "Potato": "Kentang",
    "Cucumber": "Mentimun",
    "Strawberry": "Stroberi",
    "Cabbage": "Kubis",
    "Tomato": "Tomat",
    "Corn": "Jagung",
    "Onion": "Bawang",
    "Pumpkin": "Labu",
    "Pineapple": "Nanas",
    "Eggplant": "Terong",
    "Carrot": "Wortel",
    "Sweet Potato": "Ubi Manis",
    "Spinach": "Bayam",
    "Green Pepper": "Paprika Hijau",
    "Hoe": "Cangkul",
    "Sickle": "Sabit",
    "Watering Can": "Penyiram",
    "Axe": "Kapak",
    "Hammer": "Palu",
    "Fishing Rod": "Pancingan",
    "Brush": "Sikat",
    "Milker": "Pemerah Susu",
    "Clippers": "Gunting Bulu",
    "Bell": "Lonceng",
    "Dog": "Anjing",
    "Horse": "Kuda",
    "Cow": "Sapi",
    "Sheep": "Domba",
    "Chicken": "Ayam",
    "Egg": "Telur",
    "Milk": "Susu",
    "Wool": "Bulu Domba",
    "Money": "Uang",
    "Gold": "G",
}

for en, id_text in dictionary.items():
    raw_hex = encode_hm_string(en).hex()
    add_entry(raw_hex, en, id_text)

# Also scan subfiles 2-6 for standalone words/phrases
with open('extracted/A_FILE.BIN', 'rb') as f:
    for sub in [2, 3, 4, 5, 6]:
        start = entries[sub]
        size = entries[sub+1] - start
        if size <= 0: continue
        f.seek(start)
        data = f.read(min(size, 1000000))
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
                    sent.append(table.get(w, ''))
                    j += 1
                text = ''.join(sent).strip()
                if text in dictionary:
                    raw_words = words[i:j]
                    raw_hex = struct.pack(f'<{len(raw_words)}H', *raw_words).hex()
                    add_entry(raw_hex, text, dictionary[text])
                i = j
            i += 1

print(f"Total translation entries prepared: {len(entries_toml)}")

# Generate TOML
toml_content = """# ==============================================================================
# Harvest Moon: Back to Nature (USA / SLUS-01115)
# Terjemahan Bahasa Indonesia (Native Translation Table)
# Format: psxrecomp text_xlate schema
# ==============================================================================

[localization]
default_language = "id"

"""

for e in entries_toml:
    toml_content += "[[entry]]\n"
    toml_content += f'src_hex = "{e["src_hex"]}"\n'
    en_escaped = e["en"].replace('\n', '\\n').replace('\f', '\\f').replace('"', '\\"')
    id_escaped = e["id"].replace('\n', '\\n').replace('\f', '\\f').replace('"', '\\"')
    toml_content += f'en = "{en_escaped}"\n'
    toml_content += f'id = "{id_escaped}"\n'
    toml_content += f'term = "{e["term"]}"\n\n'

target_paths = [
    "dist/HarvestMoonBTN_PC_Release/translations/harvest_moon_id.toml",
    "recomp_project/build/Release/translations/harvest_moon_id.toml",
]

for p in target_paths:
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(toml_content)
    print(f"Saved: {p} ({len(toml_content)} bytes)")
