#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════╗
║       VAULT — Password Manager               ║
║       database.json · No Encryption          ║
╚══════════════════════════════════════════════╝
"""

import json, os, sys, secrets, string
from datetime import datetime

DATABASE_FILE = "database.json"
MASTER_FILE   = "master.json"
MIN_LEN       = 12
MAX_LEN       = 128

class C:
    R      = "\033[0m"
    B      = "\033[1m"
    D      = "\033[2m"
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    BLUE   = "\033[94m"
    CYAN   = "\033[96m"
    WHITE  = "\033[97m"
    MAG    = "\033[95m"

def clr(t, *codes): return "".join(codes) + str(t) + C.R

W = 66

def load_db() -> list:
    if not os.path.exists(DATABASE_FILE):
        return []
    try:
        with open(DATABASE_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def save_db(records: list):
    tmp = DATABASE_FILE + ".tmp"
    with open(tmp, "w") as f:
        json.dump(records, f, indent=4)
    os.replace(tmp, DATABASE_FILE)


# ╔══════════════════════════════════════════════════════════════════════╗
# ║  MASTER PASSWORD                                                     ║
# ╚══════════════════════════════════════════════════════════════════════╝

def load_master() -> dict:
    if not os.path.exists(MASTER_FILE):
        return {}
    with open(MASTER_FILE, "r") as f:
        return json.load(f)

def save_master(data: dict):
    with open(MASTER_FILE, "w") as f:
        json.dump(data, f, indent=4)

def setup_master_password():
    """First run — set master password."""
    header("First Run — Set Master Password")
    warn("Set a master password to protect access to VAULT.")
    print()
    while True:
        pw1 = input(clr("  › ", C.CYAN, C.B) + clr("Set master password: ", C.WHITE))
        if len(pw1) < 4:
            err("Minimum 4 characters."); continue
        pw2 = input(clr("  › ", C.CYAN, C.B) + clr("Confirm master password: ", C.WHITE))
        if pw1 != pw2:
            err("Passwords don't match. Try again."); continue
        break

    save_master({
        "master_password": pw1,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    ok("Master password set!")
    pause()

def login():
    """Ask master password — 3 attempts then exit."""
    header("Unlock Vault")
    mdata = load_master()
    saved_pw = mdata.get("master_password", "")

    # Show saved password for recovery
    print(f"  {clr('Saved Master Password:', C.D)} {clr(saved_pw, C.YELLOW, C.B)}")
    print()

    MAX_ATTEMPTS = 3
    for attempt in range(1, MAX_ATTEMPTS + 1):
        pw = input(clr("  › ", C.CYAN, C.B) + clr("Master password: ", C.WHITE))
        if pw == saved_pw:
            ok("Access granted!")
            pause()
            return
        remaining = MAX_ATTEMPTS - attempt
        if remaining:
            err(f"Wrong password. {remaining} attempt(s) left.")
        else:
            err("Too many failed attempts. Exiting.")
            sys.exit(1)

def resolve_username(raw: str, records: list) -> str:
    base  = raw.strip().capitalize()
    count = sum(
        1 for r in records
        if r["username"].lstrip("0123456789").lower() == base.lower()
    )
    return base if count == 0 else f"{count + 1:02d}{base}"

_UP  = string.ascii_uppercase
_LO  = string.ascii_lowercase
_DG  = string.digits
_SP  = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
_ALL = _UP + _LO + _DG + _SP

def generate_password(length: int = 20) -> str:
    chars = [
        secrets.choice(_UP),
        secrets.choice(_LO),
        secrets.choice(_DG),
        secrets.choice(_SP),
        *[secrets.choice(_ALL) for _ in range(max(0, length - 4))]
    ]
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)

def generate_unique_password(length: int, records: list) -> str:
    existing = {r["password"] for r in records}
    while True:
        password = generate_password(length)
        if password not in existing:
            return password

def clear(): os.system("cls" if os.name == "nt" else "clear")
def hline(ch="─", col=C.D):    print(clr(ch * W, col))
def dline(ch="═", col=C.BLUE): print(clr(ch * W, col))

def header(title: str, sub: str = ""):
    clear()
    print()
    dline()
    print(clr(f"  🔐  VAULT  ·  {title}", C.B, C.CYAN))
    if sub: print(clr(f"  {sub}", C.D))
    dline()
    print()

def ok(m):   print(f"\n  {clr('✔', C.GREEN,  C.B)}  {clr(m, C.GREEN)}")
def err(m):  print(f"\n  {clr('✘', C.RED,    C.B)}  {clr(m, C.RED)}")
def info(m): print(f"\n  {clr('ℹ', C.CYAN,   C.B)}  {clr(m, C.WHITE)}")
def warn(m): print(f"\n  {clr('⚠', C.YELLOW, C.B)}  {clr(m, C.YELLOW)}")

def ask(label: str) -> str:
    tag = clr("  ›", C.CYAN, C.B) + " " + clr(label + ": ", C.WHITE)
    return input(tag).strip()

def confirm(msg: str) -> bool:
    return ask(f"{msg} [y/N]").lower() == "y"

def ask_length() -> int:
    raw = ask(f"Length [{MIN_LEN}–{MAX_LEN}] (Enter = 20)")
    if not raw: return 20
    try:
        n = int(raw)
        if n < MIN_LEN: warn(f"Min {MIN_LEN}. Using {MIN_LEN}."); return MIN_LEN
        if n > MAX_LEN: warn(f"Max {MAX_LEN}. Using {MAX_LEN}."); return MAX_LEN
        return n
    except ValueError:
        warn("Invalid. Using 20."); return 20

def show_record(idx, r, numbered=True):
    num  = clr(f"{idx:>3}. ", C.D) if numbered else "     "
    user = clr(r["username"], C.CYAN, C.B)
    pwd  = clr(r["password"], C.YELLOW)
    dt   = clr(r["datetime"], C.D)
    note = r.get("note", "")
    print(f"  {num}{user}")
    print(f"       {clr('Password :', C.D)} {pwd}")
    print(f"       {clr('Created  :', C.D)} {dt}")
    if note:
        print(f"       {clr('Note     :', C.D)} {clr(note, C.MAG)}")
    print()

def show_list(records, title="Records"):
    if not records: info("No records found."); return
    print()
    hline()
    print(clr(f"  {title}  —  {len(records)} record(s)", C.B, C.WHITE))
    hline()
    print()
    for i, r in enumerate(records, 1):
        show_record(i, r)
    hline()

def pause(): input(clr("\n  Press Enter to continue...", C.D))

def do_single_generate(records):
    header("Generate Password", "Single")
    raw = ask("Username / label")
    if not raw: err("Username cannot be empty."); pause(); return

    username = resolve_username(raw, records)
    if username != raw:
        print(f"\n  {clr('Auto-resolved:', C.D)} {clr(username, C.CYAN, C.B)}")

    length   = ask_length()
    note     = ask("Note (optional — Enter to skip)")
    password = generate_unique_password(length, records)

    record = {
        "username": username,
        "password": password,
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "note"    : note,
    }
    records.append(record)
    save_db(records)

    print()
    hline("─", C.GREEN)
    print(clr("  ✔  Password Generated & Saved to database.json", C.GREEN, C.B))
    hline("─", C.GREEN)
    show_record(len(records), record, numbered=False)
    pause()

def do_bulk_generate(records):
    header("Generate Password", "Bulk")
    raw_n = ask("How many passwords")
    try:
        n = int(raw_n)
        if n <= 0: raise ValueError
    except ValueError:
        err("Enter a positive integer."); pause(); return

    length    = ask_length()
    generated = []

    for i in range(1, n + 1):
        print(clr(f"\n  — Entry {i}/{n} —", C.D))
        raw = ask("Username / label")
        if not raw:
            warn(f"Skipping entry {i} — empty username."); continue

        username = resolve_username(raw, records)
        if username != raw:
            print(f"  {clr('Auto-resolved:', C.D)} {clr(username, C.CYAN, C.B)}")

        note     = ask("Note (optional)")
        password = generate_unique_password(length, records)

        record = {
            "username": username,
            "password": password,
            "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "note"    : note,
        }
        records.append(record)
        generated.append(record)
        print(clr(f"  ✔ Saved: {username}", C.GREEN))

    if generated:
        save_db(records)
        show_list(generated, "Bulk Generation Summary")
    pause()

def do_search(records):
    header("Password Manager", "Search")
    if not records: info("Database is empty."); pause(); return
    term = ask("Search username (partial, case-insensitive)")
    if not term: err("Search term cannot be empty."); pause(); return
    matches = [r for r in records if term.lower() in r["username"].lower()]
    show_list(matches, f'Results for "{term}"')
    pause()

def do_show_all(records):
    header("Password Manager", "All Records")
    show_list(records, "All Stored Passwords")
    pause()

def do_delete(records):
    header("Password Manager", "Delete Record")
    if not records: info("Database is empty."); pause(); return
    show_list(records, "Select record to delete")
    raw = ask("Record number to delete (0 to cancel)")
    try:
        idx = int(raw)
        if idx == 0: return
        if not 1 <= idx <= len(records): raise ValueError
    except ValueError:
        err("Invalid number."); pause(); return
    show_record(idx, records[idx - 1], numbered=False)
    if confirm(clr("Permanently delete this record?", C.RED)):
        records.pop(idx - 1)
        save_db(records)
        ok("Record deleted.")
    else:
        info("Cancelled.")
    pause()

def do_regenerate(records):
    header("Password Manager", "Regenerate Password")
    if not records: info("Database is empty."); pause(); return
    show_list(records, "Select record to regenerate")
    raw = ask("Record number (0 to cancel)")
    try:
        idx = int(raw)
        if idx == 0: return
        if not 1 <= idx <= len(records): raise ValueError
    except ValueError:
        err("Invalid number."); pause(); return
    show_record(idx, records[idx - 1], numbered=False)
    if confirm("Update password for this record?"):
        print()
        print(f"  {clr('[1]', C.CYAN, C.B)}  {clr('Auto Generate', C.WHITE)}")
        print(f"  {clr('[2]', C.CYAN, C.B)}  {clr('Enter Manually', C.WHITE)}")
        print()
        mode = ask("Choice")

        if mode == "1":
            length  = ask_length()
            new_pwd = generate_unique_password(length, records)
        elif mode == "2":
            while True:
                new_pwd = ask("Enter your password")
                if not new_pwd:
                    err("Password cannot be empty."); continue
                # Check uniqueness
                existing = {r["password"] for r in records}
                if new_pwd in existing:
                    err("This password already exists in database. Try another.")
                    continue
                break
        else:
            info("Cancelled."); pause(); return

        records[idx - 1]["password"] = new_pwd
        records[idx - 1]["datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_db(records)
        ok("Password updated.")
        print(f"\n  {clr('New Password:', C.D)} {clr(new_pwd, C.YELLOW, C.B)}\n")
    else:
        info("Cancelled.")
    pause()

def menu_option(num, label, desc=""):
    n = clr(f"  [{num}]", C.CYAN, C.B)
    l = clr(label, C.WHITE)
    d = clr(f"  — {desc}", C.D) if desc else ""
    print(f"{n}  {l}{d}")

def generate_menu(records):
    while True:
        header("Generate Password")
        menu_option("1", "Single Generate", "one username → one password")
        menu_option("2", "Bulk Generate",   "multiple at once")
        menu_option("0", "Back")
        print()
        ch = ask("Choice")
        if   ch == "1": do_single_generate(records)
        elif ch == "2": do_bulk_generate(records)
        elif ch == "0": break
        else: err("Invalid option."); pause()

def manager_menu(records):
    while True:
        header("Password Manager")
        menu_option("1", "Search",     "partial, case-insensitive")
        menu_option("2", "Show All",   "view every record")
        menu_option("3", "Regenerate", "new password for an entry")
        menu_option("4", "Delete",     "remove a record permanently")
        menu_option("0", "Back")
        print()
        ch = ask("Choice")
        if   ch == "1": do_search(records)
        elif ch == "2": do_show_all(records)
        elif ch == "3": do_regenerate(records)
        elif ch == "4": do_delete(records)
        elif ch == "0": break
        else: err("Invalid option."); pause()

def main_menu(records):
    while True:
        header("Main Menu", f"database.json  ·  {len(records)} record(s) stored")
        menu_option("1", "Generate Password")
        menu_option("2", "Password Manager")
        menu_option("0", "Exit")
        print()
        ch = ask("Choice")
        if ch == "1":
            generate_menu(records)
            records[:] = load_db()
        elif ch == "2":
            manager_menu(records)
            records[:] = load_db()
        elif ch == "0":
            print(clr("\n  Goodbye!\n", C.CYAN))
            sys.exit(0)
        else:
            err("Invalid option."); pause()

def main():
    # Master password check
    if not os.path.exists(MASTER_FILE):
        setup_master_password()
    login()

    records = load_db()
    main_menu(records)

if __name__ == "__main__":
    main()