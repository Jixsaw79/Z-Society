#!/usr/bin/env python3
"""Basic regression checks for the static Z-Society website; not a penetration test."""
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_CSP = (
    "default-src 'none'", "script-src 'none'", "object-src 'none'",
    "base-uri 'none'", "form-action 'none'", "frame-src 'none'",
    "connect-src 'none'", "img-src 'self' data:", "style-src 'self'",
    "style-src-attr 'none'", "font-src 'self'",
)

class AuditParser(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.errors = []
        self.ids = set()
        self.references = []
        self.csp = ""
        self.images = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "content-security-policy":
            self.csp = attrs.get("content", "")
        if tag == "script":
            self.errors.append("script element found; this site must remain zero-JavaScript")
        for name in attrs:
            if name.lower().startswith("on"):
                self.errors.append(f"inline event handler found: {name}")
            if name.lower() == "style":
                self.errors.append("inline style attribute found")
        if "id" in attrs:
            if attrs["id"] in self.ids:
                self.errors.append(f"duplicate id: {attrs['id']}")
            self.ids.add(attrs["id"])
        if tag == "img":
            self.images += 1
            if "alt" not in attrs:
                self.errors.append("image missing alt attribute")
        if tag == "a" and attrs.get("href", "").startswith("#"):
            self.references.append(attrs["href"][1:])
        if tag == "a" and attrs.get("target") == "_blank":
            rel = set(attrs.get("rel", "").lower().split())
            if not {"noopener", "noreferrer"}.issubset(rel):
                self.errors.append('target="_blank" link missing noopener noreferrer')
        if tag in ("script", "iframe", "object", "embed", "form", "base"):
            self.errors.append(f"disallowed element found: <{tag}>")

def audit_html(filename):
    parser = AuditParser(filename)
    source = (ROOT / filename).read_text(encoding="utf-8")
    parser.feed(source)
    if not parser.csp:
        parser.errors.append("Content-Security-Policy meta element missing")
    for directive in REQUIRED_CSP:
        if directive not in parser.csp:
            parser.errors.append(f"required CSP directive missing: {directive}")
    for ref in parser.references:
        if ref and ref not in parser.ids:
            parser.errors.append(f"broken in-page anchor: #{ref}")
    if not re.search(r"<title>[^<]+</title>", source, re.I):
        parser.errors.append("document title missing")
    if not re.search(r'<html[^>]+lang=', source, re.I):
        parser.errors.append("html lang attribute missing")
    for error in parser.errors:
        print(f"{filename}: {error}")
    return not parser.errors

def audit_css():
    source = (ROOT / "style.css").read_text(encoding="utf-8")
    errors = []
    if re.search(r"@import\s+url\s*\(\s*['\"]?https?://", source, re.I):
        errors.append("remote CSS @import found")
    if re.search(r"url\(\s*['\"]?https?://", source, re.I):
        errors.append("remote CSS asset found")
    for error in errors:
        print(f"style.css: {error}")
    return not errors

def main():
    ok = True
    for page in ("index.html", "404.html"):
        ok = audit_html(page) and ok
    ok = audit_css() and ok
    if ok:
        print("Static security regression checks passed.")
        return 0
    print("Static security regression checks failed.")
    return 1

if __name__ == "__main__":
    sys.exit(main())
