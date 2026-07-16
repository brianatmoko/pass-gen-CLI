# passgen 🔐

Secure password & passphrase generator — pure Python, cryptographically secure.

## Fitur

- **Password generation** — karakter acak dengan pool yang bisa dipilih (simbol, angka, huruf besar/kecil)
- **Guaranteed variety** — minimal 1 karakter dari setiap pool yang aktif
- **Passphrase generation** — kata-kata acak dari dictionary 2.650+ kata (EFF-style)
- **Entropy display** — estimasi kekuatan password dalam bits
- **Clipboard support** — `--copy` untuk salin otomatis (xclip/xsel/pbcopy/wl-copy)
- **QR code** — `--qr` untuk tampilkan QR di terminal
- **Batch generation** — `--count 10` untuk generate banyak sekaligus
- **Config persistent** — simpan preferensi di `~/.config/passgen/config.json`
- **Cryptographically secure** — pake `secrets.SystemRandom` (CSPRNG), bukan `random`
- **Zero external dependencies** — stdlib Python aja

## Instalasi

```bash
chmod +x install.sh
./install.sh
```

Pastikan `~/.local/bin` ada di PATH.

## Usage

```bash
passgen                              # 20-char password
passgen -l 32                        # 32 karakter
passgen --no-symbols                 # tanpa simbol
passgen -l 8 --no-symbols --no-numbers  # huruf saja
passgen --count 10                   # 10 password
passgen --copy                       # generate + copy ke clipboard
passgen --qr                         # tampilkan QR code

passgen passphrase                   # 4-word passphrase
passgen p -w6 --caps                 # 6 kata, capitalized
passgen p -w5 --sep _                # separator underscore

passgen estimate                     # estimasi entropy
passgen config                       # lihat konfigurasi
passgen config length 32             # set default length
passgen config no_symbols True       # default tanpa simbol
```

## Entropy Reference

| Length | Entropy (bits) | Strength |
|--------|---------------|----------|
| 8      | 52            | Moderate |
| 12     | 78            | Strong   |
| 16     | 104           | Strong   |
| 20     | 130           | Very Strong |
| 32     | 208           | Very Strong |
| 64     | 416           | Very Strong |

## Tech Stack

- Python 3.12+ — stdlib only (`secrets`, `argparse`, `math`)
- CSPRNG via `secrets.SystemRandom` (OS randomness, `/dev/urandom`)
- Wordlist: 2.650 English words
- Config: JSON di `~/.config/passgen/`

## Struktur Project

```
passgen/
├── passgen/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py         # Argparse + command handlers
│   ├── core.py        # Password/passphrase generation engine
│   ├── config.py      # Config management
│   └── wordlist.txt   # 2.650-word dictionary
├── install.sh
└── README.md
```
