#!/usr/bin/env python3

import os
import sys
import json
import subprocess
from argparse import ArgumentParser
import argcomplete

DB_PATH = os.path.expanduser("~/.local/share/pkg-tags.json")


def load_db():
    if not os.path.exists(DB_PATH):
        return {}
    with open(DB_PATH, "r") as f:
        return json.load(f)


def save_db(db):
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with open(DB_PATH, "w") as f:
        json.dump(db, f, indent=2)


def is_installed(pkg):
    return subprocess.call(["dpkg", "-s", pkg],
                           stdout=subprocess.DEVNULL,
                           stderr=subprocess.DEVNULL) == 0


def install(pkg):
    subprocess.run(["sudo", "apt", "install", "-y", pkg])


def cmd_install(args):
    pkg, tags = args.package, args.tags
    install(pkg)
    db = load_db()
    db[pkg] = sorted(set(db.get(pkg, []) + tags))
    save_db(db)


def cmd_tag(args):
    pkg, tags = args.package, args.tags
    if not is_installed(pkg):
        print(f"{pkg} non è installato.")
        sys.exit(1)
    db = load_db()
    db[pkg] = sorted(set(db.get(pkg, []) + tags))
    save_db(db)


def cmd_list(args):
    tag = args.tag
    db = load_db()
    results = [pkg for pkg, tags in db.items() if tag in tags]
    for pkg in sorted(results):
        print(pkg)


def cmd_tags(args):
    pkg = args.package
    db = load_db()
    if pkg in db:
        print(", ".join(db[pkg]))
    else:
        print(f"Nessun tag per {pkg}.")


def cmd_untag(args):
    pkg, tag = args.package, args.tag
    db = load_db()
    if pkg in db and tag in db[pkg]:
        db[pkg].remove(tag)
        if not db[pkg]:
            del db[pkg]
        save_db(db)


def cmd_remove(args):
    pkg = args.package
    db = load_db()
    if pkg in db:
        del db[pkg]
        save_db(db)


# Completer per i pacchetti (dal DB)
def package_completer(prefix, parsed_args, **kwargs):
    db = load_db()
    return [pkg for pkg in db.keys() if pkg.startswith(prefix)]


# Completer per i tag (dal DB)
def tag_completer(prefix, parsed_args, **kwargs):
    db = load_db()
    # raccolgo tutti i tag unici nel DB
    all_tags = set()
    for tags in db.values():
        all_tags.update(tags)
    return [tag for tag in all_tags if tag.startswith(prefix)]


def main():
    p = ArgumentParser(description="Tagga pacchetti APT installati")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("install")
    sp.add_argument("package")
    sp.add_argument("tags", nargs="+")  # qui i tag nuovi, non completiamo

    sp = sub.add_parser("tag")
    sp.add_argument("package").completer = package_completer
    sp.add_argument("tags", nargs="+")  # tag nuovi, senza completer

    sp = sub.add_parser("list")
    sp.add_argument("tag").completer = tag_completer

    sp = sub.add_parser("tags")
    sp.add_argument("package").completer = package_completer

    sp = sub.add_parser("untag")
    sp.add_argument("package").completer = package_completer
    sp.add_argument("tag").completer = tag_completer

    sp = sub.add_parser("remove")
    sp.add_argument("package").completer = package_completer

    argcomplete.autocomplete(p)

    args = p.parse_args()
    globals()[f"cmd_{args.cmd}"](args)


if __name__ == "__main__":
    main()
