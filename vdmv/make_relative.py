# -*- coding: utf-8 -*-
"""Convertit les liens internes absolus (/...) du site Visible dans ma ville
en liens relatifs, pour que le site fonctionne même déposé dans un
sous-dossier de l'hébergement.

Exceptions : canonical, og:url, sitemap (URLs absolues normales) et 404.html
(servie sur n'importe quel chemin par ErrorDocument, elle doit garder des
liens absolus).

Usage :  python3 vdmv/make_relative.py
"""
import re
from pathlib import Path

SITE = Path(__file__).resolve().parent / "site"


def relativize(html, depth):
    prefix = "../" * depth if depth else "./"

    def repl(m):
        attr, path = m.group(1), m.group(2)
        if path == "/":
            return f'{attr}="{prefix}"'
        if path.startswith("/#"):
            return f'{attr}="{prefix}{path[1:]}"' if depth else f'{attr}="{path[1:]}"'
        target = path.lstrip("/")
        base = "../" * depth
        return f'{attr}="{base}{target}"'

    # href/src/action internes commençant par « / » (pas //, pas http)
    return re.sub(r'(href|src|action)="(/(?!/)[^"]*)"',
                  lambda m: m.group(0) if m.group(2).startswith(("/http",)) else repl(m),
                  html)


def main():
    for f in SITE.rglob("*.html"):
        if f.name == "404.html":
            continue
        depth = len(f.relative_to(SITE).parts) - 1
        s = f.read_text()
        # protéger canonical et og/twitter (déjà absolus avec domaine, non concernés)
        out = relativize(s, depth)
        f.write_text(out)
        print(f"  ✓ {f.relative_to(SITE)} (profondeur {depth})")
    print("OK — liens internes relatifs")


if __name__ == "__main__":
    main()
