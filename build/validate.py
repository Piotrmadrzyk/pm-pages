#!/usr/bin/env python3
"""Lekka kontrola gotowych plików statycznych przed podglądem."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys

ROOT = Path(__file__).resolve().parent.parent
PAGES = [
    "index.html", "o-donie.html", "oferta.html", "realizacje.html",
    "automatyzacja.html", "akademia.html", "wycena.html", "kontakt.html",
    "blog.html", "warsztat.html", "blog/po-co-agent-malej-firmie.html",
    "warsztat/pierwsza-automatyzacja.html",
]
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids = []
        self.refs = []
        self.stack = []
        self.errors = []
        self.form_keys = []
        self.has_main = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag not in VOID:
            self.stack.append(tag)
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        if tag == "main" and attrs.get("id") == "main":
            self.has_main = True
        if tag == "form" and attrs.get("data-form-key"):
            self.form_keys.append(attrs["data-form-key"])
        for name in ("href", "src", "srcset", "data-desktop", "data-mobile"):
            if attrs.get(name):
                self.refs.append(attrs[name].split()[0])

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.errors.append("nadmiarowy </%s>" % tag)
            return
        if self.stack[-1] == tag:
            self.stack.pop()
            return
        self.errors.append("oczekiwano </%s>, znaleziono </%s>" % (self.stack[-1], tag))
        if tag in self.stack:
            while self.stack and self.stack[-1] != tag:
                self.stack.pop()
            if self.stack:
                self.stack.pop()


def local_target(page, ref):
    parts = urlsplit(ref)
    if parts.scheme or parts.netloc or ref.startswith(("mailto:", "tel:", "javascript:")):
        return None, ""
    path = unquote(parts.path)
    target = page if not path else (ROOT / page).parent.joinpath(path).resolve()
    try:
        target.relative_to(ROOT)
    except ValueError:
        return None, ""
    if target.is_dir():
        target = target / "index.html"
    return target, unquote(parts.fragment)


def main():
    problems = []
    parsed = {}
    for relative in PAGES:
        path = ROOT / relative
        if not path.exists():
            problems.append("brak strony: %s" % relative)
            continue
        parser = PageParser()
        parser.feed(path.read_text(encoding="utf-8"))
        parser.close()
        parsed[path.resolve()] = parser
        if parser.stack:
            problems.append("%s: niezamknięte znaczniki %s" % (relative, parser.stack[-5:]))
        for error in parser.errors:
            problems.append("%s: %s" % (relative, error))
        duplicates = sorted({item for item in parser.ids if parser.ids.count(item) > 1})
        if duplicates:
            problems.append("%s: powtórzone id %s" % (relative, duplicates))
        if not parser.has_main:
            problems.append("%s: brak <main id=main>" % relative)

    for path, parser in parsed.items():
        relative = path.relative_to(ROOT)
        for ref in parser.refs:
            target, fragment = local_target(relative, ref)
            if target is None:
                continue
            if not target.exists():
                problems.append("%s: niedostępny plik %s" % (relative, ref))
                continue
            if fragment and target.suffix == ".html":
                target_parser = parsed.get(target.resolve())
                if target_parser is None:
                    target_parser = PageParser()
                    target_parser.feed(target.read_text(encoding="utf-8"))
                if fragment not in target_parser.ids:
                    problems.append("%s: brak kotwicy %s w %s" % (relative, fragment, target.relative_to(ROOT)))

    keys = {key for parser in parsed.values() for key in parser.form_keys}
    expected_keys = {"kontakt", "wycena", "lista-agenty"}
    if not expected_keys.issubset(keys):
        problems.append("brak form_key: %s" % sorted(expected_keys - keys))

    css = (ROOT / "assets/site.css").read_text(encoding="utf-8")
    if css.count("{") != css.count("}"):
        problems.append("assets/site.css: niezrównoważone nawiasy")

    if problems:
        print("BŁĘDY (%d):" % len(problems))
        for problem in problems:
            print("- " + problem)
        return 1
    print("OK: %d stron, lokalne odnośniki, kotwice, identyfikatory i formularze" % len(parsed))
    return 0


if __name__ == "__main__":
    sys.exit(main())
