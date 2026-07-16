import argparse
import sys
from passgen import core, config


def do_generate(args):
    return core.generate(
        length=args.length,
        use_symbols=args.symbols,
        use_numbers=args.numbers,
        use_upper=args.upper,
        use_lower=args.lower,
    )


def cmd_generate(args):
    for i in range(args.count):
        pw, info = do_generate(args)
        prefix = f"{i+1:>3}. " if args.count > 1 else ""
        print(f"{prefix}{pw}")

    if args.count > 0:
        _copy(args.copy, pw)
        _show_entropy(info)
        if args.qr:
            _qr(pw)


def cmd_passphrase(args):
    phrase, info = core.generate_passphrase(
        num_words=args.words,
        separator=args.sep,
        capitalize=args.capitalize,
    )
    print(phrase)
    _copy(args.copy, phrase)
    _show_entropy(info)


def cmd_estimate(args):
    pool = 0
    if args.symbols:
        pool += len(core.SYMBOLS)
    if args.numbers:
        pool += len(core.NUMBERS)
    if args.upper:
        pool += len(core.UPPER)
    if args.lower:
        pool += len(core.LOWER)

    if pool == 0:
        print("No character pools selected")
        return

    print(f"  \033[1mEntropy estimation\033[0m")
    for length in [8, 12, 16, 20, 24, 32, 64, 128]:
        e = core.entropy(pool, length)
        print(f"    length {length:<4}: {e:>7.1f} bits")
    print(f"  \033[90mPool size: {pool} characters\033[0m")


def cmd_config(args):
    cfg = config.load()
    print(f"  \033[1mConfiguration\033[0m")
    for k, v in cfg.items():
        print(f"    {k:<22} = {v}")


def cmd_config_set(args):
    config.set_key(args.key, args.value)
    print(f"\033[92m\033[0m {args.key} = {args.value}")


def _copy(do_copy, text):
    if do_copy and core.copy_to_clipboard(text):
        print("\033[92m  copied to clipboard\033[0m", file=sys.stderr)


def _show_entropy(info):
    if info:
        strength = core.classify(info["pool_size"])
        print(
            f"\033[90m  entropy: {info['entropy']:.1f} bits | "
            f"pool: {info['pool_size']} chars | "
            f"strength: {strength}\033[0m",
            file=sys.stderr,
        )


def _qr(text):
    try:
        import qrcode
        qr = qrcode.QRCode(box_size=2, border=1)
        qr.add_data(text)
        qr.print_ascii()
    except ImportError:
        pass


def _build_parser():
    parser = argparse.ArgumentParser(
        prog="passgen",
        description="Secure password & passphrase generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  passgen                              # 20-char password
  passgen -l 32 --no-symbols           # 32 chars, no symbols
  passgen --count 10 --copy            # 10 passwords, clipboard
  passgen passphrase                   # 4-word passphrase
  passgen passphrase -w6 --caps        # 6 words, capitalized
  passgen estimate                     # Show entropy by length
  passgen config                       # View config
  passgen config length 32             # Set default length
""",
    )

    parser.add_argument("-l", "--length", type=int, default=config.get("length"),
                        help="Password length (default: %(default)s)")
    parser.add_argument("--symbols", action=argparse.BooleanOptionalAction,
                        default=not config.get("no_symbols"),
                        help="Include symbols (default: %(default)s)")
    parser.add_argument("--numbers", action=argparse.BooleanOptionalAction,
                        default=not config.get("no_numbers"),
                        help="Include numbers (default: %(default)s)")
    parser.add_argument("--upper", action=argparse.BooleanOptionalAction,
                        default=not config.get("no_upper"),
                        help="Include uppercase (default: %(default)s)")
    parser.add_argument("--lower", action=argparse.BooleanOptionalAction,
                        default=not config.get("no_lower"),
                        help="Include lowercase (default: %(default)s)")
    parser.add_argument("--count", "-c", type=int, default=1,
                        help="Number of passwords (default: 1)")
    parser.add_argument("--copy", action="store_true",
                        help="Copy first password to clipboard")
    parser.add_argument("--no-entropy", dest="show_entropy", action="store_false",
                        help="Hide entropy info")
    parser.add_argument("--qr", action="store_true",
                        help="Show QR code in terminal")

    sub = parser.add_subparsers(dest="command")

    p_phrase = sub.add_parser("passphrase", aliases=["p"],
                              help="Generate memorable passphrase")
    p_phrase.add_argument("-w", "--words", type=int, default=config.get("passphrase_words"),
                          help="Number of words (default: %(default)s)")
    p_phrase.add_argument("--sep", "-s", default=config.get("passphrase_sep"),
                          help="Word separator (default: '%(default)s')")
    p_phrase.add_argument("--caps", "--capitalize", dest="capitalize",
                          action="store_true", help="Capitalize words")
    p_phrase.add_argument("--copy", action="store_true")
    p_phrase.add_argument("--no-entropy", dest="show_entropy", action="store_false")
    p_phrase.set_defaults(func=cmd_passphrase)

    p_est = sub.add_parser("estimate", aliases=["entropy"],
                           help="Estimate entropy for given settings")
    p_est.add_argument("--no-symbols", dest="symbols", action="store_false")
    p_est.add_argument("--no-numbers", dest="numbers", action="store_false")
    p_est.add_argument("--no-upper", dest="upper", action="store_false")
    p_est.add_argument("--no-lower", dest="lower", action="store_false")
    p_est.set_defaults(func=cmd_estimate)

    p_cfg = sub.add_parser("config", help="View configuration")
    p_cfg.set_defaults(func=cmd_config)

    p_cfg_set = sub.add_parser("config-set", help="Set configuration key=value")
    p_cfg_set.add_argument("key", help="Config key")
    p_cfg_set.add_argument("value", help="Config value")
    p_cfg_set.set_defaults(func=cmd_config_set)

    return parser


def main():
    parser = _build_parser()
    args, _ = parser.parse_known_args()

    if args.command:
        args.func(args)
        return

    # No subcommand → generate password
    for i in range(args.count):
        pw, info = do_generate(args)
        prefix = f"{i+1:>3}. " if args.count > 1 else ""
        print(f"{prefix}{pw}")

    if args.count > 0:
        _copy(args.copy, pw)
        if args.show_entropy:
            _show_entropy(info)
        if args.qr:
            _qr(pw)


if __name__ == "__main__":
    main()
