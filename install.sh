#!/usr/bin/env bash
set -euo pipefail

BIN_DIR="$HOME/.local/bin"
LIB_DIR="$HOME/.local/lib/passgen"

mkdir -p "$BIN_DIR" "$LIB_DIR"

cp -r passgen "$LIB_DIR/"

cat > "$BIN_DIR/passgen" << 'SCRIPT'
#!/usr/bin/env bash
exec python3 -m passgen "$@"
SCRIPT

chmod +x "$BIN_DIR/passgen"

echo "passgen v2 terinstal!"
echo "  Jalankan: passgen"
echo "  Pastikan $BIN_DIR ada di PATH"
