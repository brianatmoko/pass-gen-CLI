#!/usr/bin/env python3
import argparse
import ctypes
import os
import sys

def main():
    lib_path = os.path.join(os.path.dirname(__file__), "libpassgen.so")
    if not os.path.exists(lib_path):
        lib_dir = os.path.expanduser("~/.local/lib/passgen")
        lib_path = os.path.join(lib_dir, "libpassgen.so")

    try:
        lib = ctypes.CDLL(lib_path)
    except OSError as e:
        print(f"Error: cannot load libpassgen.so — {e}", file=sys.stderr)
        print("Run 'make' or 'install.sh' first", file=sys.stderr)
        sys.exit(1)

    lib.generate.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_uint]
    lib.generate.restype = ctypes.c_int

    parser = argparse.ArgumentParser(description="passgen — secure password (C++ engine)")
    parser.add_argument("--length", "-l", type=int, default=16, help="Password length")
    parser.add_argument("--no-symbols", action="store_true", help="Exclude symbols")
    parser.add_argument("--no-numbers", action="store_true", help="Exclude numbers")
    parser.add_argument("--no-upper", action="store_true", help="Exclude uppercase")
    parser.add_argument("--no-lower", action="store_true", help="Exclude lowercase")
    args = parser.parse_args()

    flags = 0
    if not args.no_symbols: flags |= 1
    if not args.no_numbers: flags |= 2
    if not args.no_upper:   flags |= 4
    if not args.no_lower:   flags |= 8

    buf = ctypes.create_string_buffer(args.length + 1)
    ret = lib.generate(buf, args.length, flags)

    if ret < 0:
        print("Error: password generation failed", file=sys.stderr)
        sys.exit(1)

    print(buf.value.decode())

if __name__ == "__main__":
    main()
