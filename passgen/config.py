import os
import json

CONFIG_DIR = os.path.expanduser("~/.config/passgen")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

DEFAULTS = {
    "length": 20,
    "no_symbols": False,
    "no_numbers": False,
    "no_upper": False,
    "no_lower": False,
    "passphrase_words": 4,
    "passphrase_sep": "-",
    "copy_to_clipboard": True,
    "show_entropy": True,
}


def ensure_dir():
    os.makedirs(CONFIG_DIR, exist_ok=True)


def load():
    ensure_dir()
    if not os.path.exists(CONFIG_FILE):
        return dict(DEFAULTS)
    try:
        with open(CONFIG_FILE) as f:
            return {**DEFAULTS, **json.load(f)}
    except (json.JSONDecodeError, IOError):
        return dict(DEFAULTS)


def save(cfg):
    ensure_dir()
    with open(CONFIG_FILE, "w") as f:
        json.dump(cfg, f, indent=2)


def get(key):
    return load().get(key, DEFAULTS.get(key))


def set_key(key, val):
    cfg = load()
    cfg[key] = val
    save(cfg)
