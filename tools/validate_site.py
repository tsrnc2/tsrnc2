#!/usr/bin/env python3
"""Validate the static C/C++ consulting site with only the Python standard library."""

from __future__ import annotations

import json
import posixpath
from datetime import datetime, timezone
import re
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = "https://jacob-wood-cpp-consulting.onrender.com"
SALE_END = datetime.fromisoformat("2027-01-01T00:00:00-08:00").astimezone(timezone.utc)

PRIMARY_PAGES = {
    "index.html": f"{BASE_URL}/",
    "experience.html": f"{BASE_URL}/experience.html",
    "checkout.html": f"{BASE_URL}/checkout.html",
}
BASIC_PAGES = {
    "basic/index.html": ("index.html", f"{BASE_URL}/"),
    "basic/experience.html": ("experience.html", f"{BASE_URL}/experience.html"),
    "basic/checkout.html": ("checkout.html", f"{BASE_URL}/checkout.html"),
}
REQUIRED_FILES = {
    *PRIMARY_PAGES,
    *BASIC_PAGES,
    "404.html",
    "styles.css",
    "app.js",
    "sale.js",
    "checkout.js",
    "checkout-config.js",
    "favicon.svg",
    "site.webmanifest",
    "robots.txt",
    "sitemap.xml",
    "README.md",
    "DEPLOYMENT.md",
}

ALLOWED_EXTERNAL_SCHEMES = {"http", "https", "mailto", "tel"}
CARD_FIELD_NAMES = {
    "card", "cardnumber", "card-number", "cc-number", "cc-exp", "cc-csc",
    "cvc", "cvv", "expiry", "expiration",
}


class SiteHTMLParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.attrs: list[tuple[str, dict[str, str]]] = []
        self.ids: set[str] = set()
        self.names: set[str] = set()
        self.hrefs: list[str] = []
        self.srcs: list[str] = []
        self.scripts = 0
        self.styles = 0
        self.title_depth = 0
        self.title_text: list[str] = []
        self.html_lang = ""
        self.meta: list[dict[str, str]] = []
        self.links: list[dict[str, str]] = []
        self.inputs: list[dict[str, str]] = []
        self.media_tags: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = {key.lower(): (value or "") for key, value in attrs}
        tag = tag.lower()
        self.attrs.append((tag, values))
        if tag == "html":
            self.html_lang = values.get("lang", "")
        if "id" in values:
            self.ids.add(values["id"])
        if "name" in values:
            self.names.add(values["name"])
        if "href" in values:
            self.hrefs.append(values["href"])
        if "src" in values:
            self.srcs.append(values["src"])
        if tag == "script":
            self.scripts += 1
        elif tag == "style":
            self.styles += 1
        elif tag == "title":
            self.title_depth += 1
        elif tag == "meta":
            self.meta.append(values)
        elif tag == "link":
            self.links.append(values)
        elif tag == "input":
            self.inputs.append(values)
        elif tag in {"img", "picture", "video", "audio", "canvas", "svg"}:
            self.media_tags.append(tag)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title" and self.title_depth:
            self.title_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.title_depth:
            self.title_text.append(data)


def parse_html(path: str) -> SiteHTMLParser:
    parser = SiteHTMLParser()
    parser.feed((ROOT / path).read_text(encoding="utf-8"))
    parser.close()
    return parser


def meta_content(parser: SiteHTMLParser, key: str, value: str) -> str | None:
    key = key.lower()
    value = value.lower()
    for row in parser.meta:
        if row.get(key, "").lower() == value:
            return row.get("content")
    return None


def link_href(parser: SiteHTMLParser, rel_value: str) -> str | None:
    wanted = rel_value.lower()
    for row in parser.links:
        rels = {part.lower() for part in row.get("rel", "").split()}
        if wanted in rels:
            return row.get("href")
    return None


def normalized_target(source: str, raw_url: str) -> tuple[str | None, str]:
    parsed = urlsplit(raw_url)
    scheme = parsed.scheme.lower()
    if scheme:
        if scheme not in ALLOWED_EXTERNAL_SCHEMES:
            raise ValueError(f"unsupported URL scheme {scheme!r}")
        return None, parsed.fragment
    if raw_url.startswith("//"):
        return None, parsed.fragment

    raw_path = parsed.path
    if not raw_path:
        target = source
    elif raw_path.startswith("/"):
        target = raw_path.lstrip("/")
    else:
        target = posixpath.join(str(PurePosixPath(source).parent), raw_path)

    target = posixpath.normpath(target)
    if target in {"", "."}:
        target = "index.html"
    if target.startswith("../") or target == "..":
        raise ValueError("path escapes repository root")
    if target.endswith("/"):
        target += "index.html"
    return target, parsed.fragment


def valid_stripe_link(value: str) -> bool:
    if not value:
        return True
    if re.search(r"[\x00-\x20\x7f]", value):
        return False
    try:
        parsed = urlsplit(value)
        port = parsed.port
    except ValueError:
        return False
    return (
        parsed.scheme == "https"
        and parsed.hostname == "buy.stripe.com"
        and parsed.username is None
        and parsed.password is None
        and port is None
        and re.fullmatch(r"/[A-Za-z0-9_]+", parsed.path or "") is not None
    )


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    def check(condition: bool, message: str) -> None:
        if not condition:
            errors.append(message)

    for relative in sorted(REQUIRED_FILES):
        check((ROOT / relative).is_file(), f"missing required file: {relative}")

    html_paths = sorted((*PRIMARY_PAGES.keys(), *BASIC_PAGES.keys(), "404.html"))
    parsed_docs: dict[str, SiteHTMLParser] = {}
    for relative in html_paths:
        if (ROOT / relative).is_file():
            try:
                parsed_docs[relative] = parse_html(relative)
            except Exception as exc:  # pragma: no cover - defensive CI output
                errors.append(f"{relative}: HTML parsing failed: {exc}")

    for relative, parser in parsed_docs.items():
        check(parser.html_lang.lower().startswith("en"), f"{relative}: missing English html lang")
        check(bool("".join(parser.title_text).strip()), f"{relative}: missing title")
        check(
            any(row.get("charset", "").lower() == "utf-8" for row in parser.meta),
            f"{relative}: missing UTF-8 charset",
        )
        check(
            meta_content(parser, "name", "viewport") is not None,
            f"{relative}: missing viewport meta",
        )

        for field in parser.inputs:
            input_type = field.get("type", "text").lower()
            name = field.get("name", "").lower()
            autocomplete = field.get("autocomplete", "").lower()
            sensitive = (
                input_type in {"number", "tel", "password"}
                or name in CARD_FIELD_NAMES
                or autocomplete.startswith("cc-")
            )
            check(not sensitive, f"{relative}: local payment/card input is prohibited: {field}")

    for relative, expected_canonical in PRIMARY_PAGES.items():
        parser = parsed_docs.get(relative)
        if parser is None:
            continue
        check(link_href(parser, "canonical") == expected_canonical, f"{relative}: wrong canonical URL")
        check(link_href(parser, "stylesheet") == "styles.css", f"{relative}: missing main stylesheet")
        check("app.js" in parser.srcs, f"{relative}: missing app.js")
        basic_target = f"basic/{relative}"
        check(
            any(urlsplit(href).path == basic_target for href in parser.hrefs),
            f"{relative}: missing Basic HTML link to {basic_target}",
        )

    for relative, (graphics_name, expected_canonical) in BASIC_PAGES.items():
        parser = parsed_docs.get(relative)
        if parser is None:
            continue
        check(link_href(parser, "canonical") == expected_canonical, f"{relative}: wrong canonical URL")
        robots = meta_content(parser, "name", "robots") or ""
        check("noindex" in robots.lower(), f"{relative}: Basic HTML mirror must be noindex")
        check(parser.scripts == 0, f"{relative}: Basic HTML mirror contains script tags")
        check(parser.styles == 0, f"{relative}: Basic HTML mirror contains style tags")
        check(link_href(parser, "stylesheet") is None, f"{relative}: Basic HTML mirror loads CSS")
        check(not parser.media_tags, f"{relative}: Basic HTML mirror contains media: {parser.media_tags}")
        expected_graphics = f"../{graphics_name}"
        check(
            any(urlsplit(href).path == expected_graphics for href in parser.hrefs),
            f"{relative}: missing graphics-version link to {expected_graphics}",
        )

    all_known_files = {
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file() and ".git" not in path.parts
    }
    for relative, parser in parsed_docs.items():
        for attribute, raw_url in [("href", url) for url in parser.hrefs] + [
            ("src", url) for url in parser.srcs
        ]:
            try:
                target, fragment = normalized_target(relative, raw_url)
            except ValueError as exc:
                errors.append(f"{relative}: invalid {attribute}={raw_url!r}: {exc}")
                continue
            if target is None:
                continue
            check(target in all_known_files, f"{relative}: broken {attribute} target {raw_url!r} -> {target}")
            if fragment and target in parsed_docs:
                target_parser = parsed_docs[target]
                check(
                    fragment in target_parser.ids or fragment in target_parser.names,
                    f"{relative}: broken fragment {raw_url!r}",
                )

    index_text = (ROOT / "index.html").read_text(encoding="utf-8")
    checkout_text = (ROOT / "checkout.html").read_text(encoding="utf-8")
    basic_checkout_text = (ROOT / "basic/checkout.html").read_text(encoding="utf-8")
    sale_text = (ROOT / "sale.js").read_text(encoding="utf-8")
    checkout_js = (ROOT / "checkout.js").read_text(encoding="utf-8")

    for label, text in {
        "index.html": index_text,
        "checkout.html": checkout_text,
        "basic/checkout.html": basic_checkout_text,
    }.items():
        check("$100" in text, f"{label}: missing $100 single-lesson price")
        check("$1,000" in text, f"{label}: missing $1,000 regular course price")
        check("$400" in text, f"{label}: missing $400 sale course price")

    check("2027-01-01T00:00:00-08:00" in sale_text, "sale.js: wrong or missing sale end time")
    check('salePrice: "400"' in sale_text, "sale.js: wrong sale price")
    check('regularPrice: "1,000"' in sale_text, "sale.js: wrong regular price")
    check(
        'document.documentElement.classList.add("sale-js-active")' in sale_text,
        "sale.js: missing no-JavaScript-safe activation class",
    )
    styles_text = (ROOT / "styles.css").read_text(encoding="utf-8")
    check(
        "html:not(.sale-js-active) [data-sale-on]" in styles_text
        and "html:not(.sale-js-active) [data-sale-off]" in styles_text,
        "styles.css: missing conservative no-JavaScript sale fallback",
    )
    if datetime.now(timezone.utc) >= SALE_END:
        check(
            "New Year sale" not in index_text
            and "New Year sale" not in checkout_text
            and "New Year sale" not in basic_checkout_text,
            "expired New Year sale copy remains in published pages",
        )
    check("window.COURSE_SALE" in checkout_js, "checkout.js: sale state is not consumed")
    check("buy.stripe.com" in checkout_js, "checkout.js: Stripe hostname boundary missing")
    check("window.location.assign" in checkout_js, "checkout.js: user-initiated checkout navigation missing")

    config_text = (ROOT / "checkout-config.js").read_text(encoding="utf-8")
    entries = dict(re.findall(r"\b(single|course)\s*:\s*\"([^\"]*)\"", config_text))
    for key in ("single", "course"):
        check(key in entries, f"checkout-config.js: missing {key!r} entry")
        if key in entries:
            check(valid_stripe_link(entries[key]), f"checkout-config.js: invalid {key} Stripe URL")
    if any(entries.get(key) for key in ("single", "course")):
        warnings.append(
            "Stripe links are configured; provider-side product, amount, currency, sale expiry, "
            "and payment status still require independent verification."
        )
    else:
        warnings.append("Stripe links are blank; online payment remains safely fail-closed.")

    try:
        manifest = json.loads((ROOT / "site.webmanifest").read_text(encoding="utf-8"))
        check(manifest.get("start_url") == "./index.html", "site.webmanifest: unexpected start_url")
        check(bool(manifest.get("icons")), "site.webmanifest: icons missing")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"site.webmanifest: invalid JSON: {exc}")

    try:
        tree = ET.parse(ROOT / "sitemap.xml")
        namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = {node.text for node in tree.findall(".//sm:loc", namespace)}
        expected_urls = set(PRIMARY_PAGES.values())
        check(urls == expected_urls, f"sitemap.xml: expected {sorted(expected_urls)}, got {sorted(urls)}")
    except (OSError, ET.ParseError) as exc:
        errors.append(f"sitemap.xml: invalid XML: {exc}")

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    check("User-agent: *" in robots, "robots.txt: missing wildcard user-agent")
    check("Allow: /" in robots, "robots.txt: missing Allow directive")
    check(f"Sitemap: {BASE_URL}/sitemap.xml" in robots, "robots.txt: wrong sitemap URL")

    if warnings:
        for warning in warnings:
            print(f"WARNING: {warning}", file=sys.stderr)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"Site validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    print(
        "Site validation passed: "
        f"{len(REQUIRED_FILES)} required files, {len(parsed_docs)} HTML pages, "
        "internal links/fragments, canonical metadata, pricing, sale state, "
        "checkout safety, manifest, robots, and sitemap."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
