#!/usr/bin/env python3
"""Generate an llms.txt file from a sitemap (URL or local file).

Follows the llmstxt.org convention: an H1 site name, a blockquote summary,
then H2 sections containing markdown link lists. Pages are grouped by the
first URL path segment, and secondary pages go into a section named "Optional".

Standard library only, Python 3.9+. See README.md for usage and limitations.
"""
import argparse
import re
import sys
import time
import urllib.error
import urllib.request
import urllib.robotparser
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from urllib.parse import urldefrag, urlparse

DEFAULT_UA = "llms-txt-generator/1.0 (+https://github.com/Usama-Afzall/geo-aeo-toolkit)"
MAX_BYTES = 2_000_000  # never read more than ~2 MB from one response
# First path segments that usually hold secondary pages (override with --optional).
DEFAULT_OPTIONAL = {"privacy", "privacy-policy", "terms", "legal", "policies", "cookies",
                    "tag", "tags", "author", "authors", "cart", "account", "login"}


class MetaParser(HTMLParser):
    """Collects <title> and the meta description (og:description as fallback)."""

    def __init__(self):
        super().__init__()
        self.title, self.description, self.og_description = "", "", ""
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "title":
            self._in_title = True
        elif tag == "meta":
            name = (a.get("name") or a.get("property") or "").lower()
            if name == "description" and not self.description:
                self.description = a.get("content") or ""
            elif name == "og:description" and not self.og_description:
                self.og_description = a.get("content") or ""

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data


def clean(text):
    """Collapse whitespace so each entry stays on one line."""
    return re.sub(r"\s+", " ", text or "").strip()


def log(msg):
    print(msg, file=sys.stderr)


def http_get(url, ua, timeout):
    """Return (bytes, content_type, charset). Raises urllib errors on failure."""
    req = urllib.request.Request(url, headers={"User-Agent": ua})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read(MAX_BYTES + 1)[:MAX_BYTES]
        return data, resp.headers.get_content_type(), resp.headers.get_content_charset()


def load_xml(source, ua, timeout):
    """Load a sitemap from a URL or local path and return its root element."""
    if re.match(r"^https?://", source, re.I):
        data, _, _ = http_get(source, ua, timeout)
    else:
        with open(source, "rb") as fh:
            data = fh.read()
    return ET.fromstring(data)


def locs(root, child_tag):
    """Return <loc> values of every <child_tag> element, ignoring XML namespaces."""
    out = []
    for el in root.iter():
        if el.tag.split("}")[-1] == child_tag:
            for sub in el:
                if sub.tag.split("}")[-1] == "loc" and sub.text:
                    out.append(sub.text.strip())
    return out


def collect_urls(source, ua, timeout):
    """Expand a sitemap, following a sitemap index exactly one level deep."""
    root = load_xml(source, ua, timeout)
    kind = root.tag.split("}")[-1]
    if kind == "urlset":
        return locs(root, "url")
    if kind != "sitemapindex":
        raise ValueError("root element is <%s>, expected <urlset> or <sitemapindex>" % kind)
    urls = []
    for child in locs(root, "sitemap"):
        try:
            child_root = load_xml(child, ua, timeout)
        except (urllib.error.URLError, ET.ParseError, OSError, ValueError) as exc:
            log("warn: skipping child sitemap %s (%s)" % (child, exc))
            continue
        if child_root.tag.split("}")[-1] == "urlset":
            urls.extend(locs(child_root, "url"))
        else:
            log("warn: %s is a nested index; only one level is followed" % child)
    return urls


class Robots:
    """Per-origin robots.txt cache built on urllib.robotparser."""

    def __init__(self, ua, timeout):
        self.ua, self.timeout, self.cache = ua, timeout, {}

    def allowed(self, url):
        p = urlparse(url)
        origin = "%s://%s" % (p.scheme, p.netloc)
        if origin not in self.cache:
            rp = urllib.robotparser.RobotFileParser()
            try:
                data, _, _ = http_get(origin + "/robots.txt", self.ua, self.timeout)
                rp.parse(data.decode("utf-8", "replace").splitlines())
            except urllib.error.HTTPError as exc:
                # Same convention as RobotFileParser: 401/403 means closed, other 4xx means open.
                if exc.code in (401, 403):
                    rp.disallow_all = True
                else:
                    rp.allow_all = True
            except (urllib.error.URLError, OSError):
                log("warn: could not read robots.txt for %s; assuming allowed" % origin)
                rp.allow_all = True
            self.cache[origin] = rp
        return self.cache[origin].can_fetch(self.ua, url)


def fetch_page(url, ua, timeout):
    """Return (title, description) for an HTML page, or None if it is not HTML."""
    data, ctype, charset = http_get(url, ua, timeout)
    if ctype not in ("text/html", "application/xhtml+xml"):
        return None
    try:
        text = data.decode(charset or "utf-8", "replace")
    except LookupError:
        text = data.decode("utf-8", "replace")
    parser = MetaParser()
    parser.feed(text)
    return clean(parser.title), clean(parser.description or parser.og_description)


def section_of(url, optional):
    """Return the section name for a URL, based on its first path segment."""
    segs = [s for s in urlparse(url).path.split("/") if s]
    if not segs:
        return "Main"
    first = segs[0].lower()
    if first in optional or (len(segs) == 1 and first.rsplit(".", 1)[0] in optional):
        return "Optional"
    if len(segs) == 1:
        return "Main"  # top-level pages such as /about
    return first.replace("-", " ").replace("_", " ").title()


def md_link(title, url, desc):
    """One markdown list entry; brackets in titles are escaped."""
    title = title.replace("[", "\\[").replace("]", "\\]") or url
    return "- [%s](%s)%s" % (title, url, ": " + desc if desc else "")


def render(site, summary, entries, optional):
    """Build the llms.txt text. entries: list of (url, title, desc)."""
    groups = {}
    for url, title, desc in entries:
        groups.setdefault(section_of(url, optional), []).append((url, title, desc))
    lines = ["# " + site, "", "> " + summary, ""]
    names = sorted(n for n in groups if n not in ("Main", "Optional"))
    for name in [n for n in ["Main"] + names + ["Optional"] if n in groups]:
        lines += ["## " + name, ""]
        lines += [md_link(t, u, d) for u, t, d in sorted(groups[name])]
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_parser():
    ap = argparse.ArgumentParser(description="Generate llms.txt from a sitemap URL or local sitemap.xml.")
    ap.add_argument("sitemap", help="sitemap URL or path to a local sitemap.xml (index files supported)")
    ap.add_argument("-o", "--output", default="llms.txt", help="output file (default: llms.txt)")
    ap.add_argument("--site-name", help="H1 text (default: homepage title, else the hostname)")
    ap.add_argument("--summary", help="blockquote summary (default: homepage meta description)")
    ap.add_argument("--dry-run", action="store_true", help="print the result to stdout, write no file")
    ap.add_argument("--max-pages", type=int, default=50, help="maximum pages to fetch (default: 50)")
    ap.add_argument("--delay", type=float, default=1.0, help="seconds between page requests (default: 1.0)")
    ap.add_argument("--timeout", type=float, default=10.0, help="per-request timeout in seconds (default: 10)")
    ap.add_argument("--user-agent", default=DEFAULT_UA, help="User-Agent string, also used for robots.txt matching")
    ap.add_argument("--optional", default="", help="extra comma separated first path segments for the Optional section")
    return ap


def main(argv=None):
    args = build_parser().parse_args(argv)
    optional = DEFAULT_OPTIONAL | {s.strip().lower() for s in args.optional.split(",") if s.strip()}
    try:
        urls = collect_urls(args.sitemap, args.user_agent, args.timeout)
    except (urllib.error.URLError, ET.ParseError, OSError, ValueError) as exc:
        log("error: cannot read sitemap %s: %s" % (args.sitemap, exc))
        return 2

    seen, queue = set(), []
    for u in urls:
        u = urldefrag(u)[0]
        if urlparse(u).scheme in ("http", "https") and u not in seen:
            seen.add(u)
            queue.append(u)
    if not queue:
        log("error: the sitemap contains no http(s) URLs")
        return 1
    host = urlparse(queue[0]).netloc
    robots, entries, skipped = Robots(args.user_agent, args.timeout), [], 0
    homepage = None

    for url in queue:
        if len(entries) >= args.max_pages:
            log("info: reached --max-pages (%d)" % args.max_pages)
            break
        if urlparse(url).netloc != host:
            log("skip (other host): " + url)
            continue
        if not robots.allowed(url):
            log("skip (robots.txt): " + url)
            skipped += 1
            continue
        try:
            result = fetch_page(url, args.user_agent, args.timeout)
        except urllib.error.HTTPError as exc:
            log("skip (HTTP %d): %s" % (exc.code, url))
            continue
        except (urllib.error.URLError, OSError, ValueError) as exc:
            log("skip (%s): %s" % (exc, url))
            continue
        if result is None:
            log("skip (not HTML): " + url)
        else:
            log("ok: " + url)
            entries.append((url, result[0], result[1]))
            if not urlparse(url).path.strip("/") and homepage is None:
                homepage = result
        time.sleep(max(args.delay, 0))

    if not entries:
        log("error: no pages could be fetched (%d skipped by robots.txt)" % skipped)
        return 1
    home = homepage or ("", "")
    site = args.site_name or home[0] or host
    summary = args.summary or home[1] or "Pages from %s, listed from its sitemap." % host
    text = render(clean(site), clean(summary), entries, optional)
    if args.dry_run:
        sys.stdout.write(text)
        return 0
    try:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(text)
    except OSError as exc:
        log("error: cannot write %s: %s" % (args.output, exc))
        return 1
    log("wrote %s (%d pages)" % (args.output, len(entries)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
