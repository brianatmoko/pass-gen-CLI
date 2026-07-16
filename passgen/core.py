import secrets
import math
import string

SYMBOLS = "!@#$%^&*()-_=+[]{}|;:,.<>?/~"
NUMBERS = string.digits
UPPER = string.ascii_uppercase
LOWER = string.ascii_lowercase

POOL_NAMES = {
    "symbols": SYMBOLS,
    "numbers": NUMBERS,
    "upper": UPPER,
    "lower": LOWER,
}


def build_pool(use_symbols=True, use_numbers=True, use_upper=True, use_lower=True):
    pools = []
    if use_symbols:
        pools.append(SYMBOLS)
    if use_numbers:
        pools.append(NUMBERS)
    if use_upper:
        pools.append(UPPER)
    if use_lower:
        pools.append(LOWER)

    if not pools:
        pools = [UPPER, LOWER]

    return pools


def entropy(pool_size, length):
    if pool_size <= 0 or length <= 0:
        return 0.0
    return length * math.log2(pool_size)


def classify(pool_size):
    if pool_size >= 72:
        return "very strong"
    if pool_size >= 52:
        return "strong"
    if pool_size >= 36:
        return "moderate"
    return "weak"


def generate(
    length=None,
    use_symbols=True,
    use_numbers=True,
    use_upper=True,
    use_lower=True,
):
    length = length or 20
    pools = build_pool(use_symbols, use_numbers, use_upper, use_lower)

    all_chars = "".join(pools)
    total_pool = len(all_chars)

    if total_pool == 0:
        raise ValueError("No character pool available")

    guaranteed = bytearray([0]) * length
    idx = 0
    for pool in pools:
        if idx < length:
            guaranteed[idx] = ord(pool[secrets.randbelow(len(pool))])
            idx += 1

    # Fill remaining positions from full pool
    for i in range(idx, length):
        guaranteed[i] = ord(all_chars[secrets.randbelow(total_pool)])

    # Fisher-Yates shuffle to distribute guaranteed chars
    ba = bytearray(guaranteed)
    for i in range(length - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        ba[i], ba[j] = ba[j], ba[i]

    pw = ba.decode()

    return pw, {
        "length": length,
        "pool_size": total_pool,
        "entropy": entropy(total_pool, length),
        "pools_used": len(pools),
    }


def generate_passphrase(num_words=4, separator="-", capitalize=False):
    words = load_wordlist()
    chosen = []
    for _ in range(num_words):
        w = secrets.choice(words)
        if capitalize:
            w = w.capitalize()
        chosen.append(w)

    phrase = separator.join(chosen)

    pool_est = len(words)
    total_entropy = entropy(pool_est, num_words)

    return phrase, {
        "num_words": num_words,
        "pool_size": pool_est,
        "entropy": total_entropy,
    }


def load_wordlist():
    try:
        from importlib.resources import files
        data = files("passgen").joinpath("wordlist.txt").read_text().splitlines()
        if data:
            return data
    except Exception:
        pass

    # fallback wordlist (100 common English words)
    return [
        "apple", "beach", "chair", "dance", "eagle", "flame", "grape", "house",
        "igloo", "joker", "knife", "lemon", "mango", "night", "ocean", "piano",
        "queen", "river", "snake", "tiger", "umbra", "vivid", "whale", "xenon",
        "yacht", "zebra", "angel", "brave", "cloud", "delta", "ember", "fable",
        "ghost", "happy", "index", "jewel", "kebab", "latch", "magic", "noble",
        "orbit", "plaza", "quota", "raven", "solar", "tower", "ultra", "vigor",
        "waltz", "xerox", "young", "zonal", "bacon", "crisp", "drift", "evoke",
        "froze", "grasp", "hazel", "image", "jolly", "kayak", "lunar", "mirth",
        "nanny", "olive", "pivot", "quilt", "radar", "sauce", "taint", "usher",
        "vocal", "wrist", "anvil", "bliss", "cramp", "dwarf", "envoy", "flair",
        "gland", "hiker", "inlet", "jumbo", "koala", "llama", "motel", "nymph",
        "opera", "pixel", "quill", "rivet", "swirl", "tulip", "unity", "visor",
        "wagon", "alarm", "bloom", "coral", "daisy", "elbow",
    ]


def copy_to_clipboard(text):
    import subprocess
    import shutil

    if shutil.which("xclip"):
        subprocess.run(["xclip", "-selection", "clipboard"], input=text.encode(), check=False)
        return True
    if shutil.which("xsel"):
        subprocess.run(["xsel", "--clipboard", "--input"], input=text.encode(), check=False)
        return True
    if shutil.which("pbcopy"):
        subprocess.run(["pbcopy"], input=text.encode(), check=False)
        return True
    if shutil.which("clip.exe"):
        subprocess.run(["clip.exe"], input=text.encode(), check=False)
        return True
    if shutil.which("wl-copy"):
        subprocess.run(["wl-copy"], input=text.encode(), check=False)
        return True
    return False
