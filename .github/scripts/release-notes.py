#!/usr/bin/env python3
"""
Turns the release notes GitHub generates for a release (Markdown) into the other places they belong.

  release-notes.py normalize <notes.md>
      Wraps @words in pull request titles (e.g. "@controller", "@service") in backticks, so GitHub doesn't treat
      them as user mentions and notify whoever owns that username. The authors stay mentions.

  release-notes.py changelog <CHANGELOG.md> <version> <date> <notes.md>
      Prepends a "## v<version> (<date>)" section with the notes to CHANGELOG.md.

  release-notes.py change-notes <plugin.xml> <notes.md> <release-url>
      Replaces CHANGELOG_PLACEHOLDER in plugin.xml with the notes as HTML, for the IDE's plugin update dialog.

Only the Markdown that GitHub's generated notes use is handled: headings, "* " list items, **bold**, `code`,
author @mentions and bare URLs.
"""
import html
import re
import sys

URL = re.compile(r"https?://[^\s)]+")
BOLD = re.compile(r"\*\*(.+?)\*\*")
CODE = re.compile(r"`([^`]+)`")
PULL = re.compile(r"/pull/(\d+)$")
# "* <title> by @author in <url>"
PULL_ITEM = re.compile(r"^(\* )(.*)( by @[A-Za-z0-9-]+ in https?://\S+)$")
# the author in "<title> by @author in <url>" and "@author made their first contribution in <url>"
AUTHOR = re.compile(r"(?:\bby |^)@([A-Za-z0-9][A-Za-z0-9-]*)(?= in | made their first)")


def normalize(notes_path):
    lines = []
    for line in open(notes_path, encoding="utf-8").read().splitlines():
        match = PULL_ITEM.match(line)
        if match:
            title = re.sub(r"(?<![\w`])(@[\w-]+)", r"`\1`", match.group(2))
            line = match.group(1) + title + match.group(3)
        lines.append(line)
    open(notes_path, "w", encoding="utf-8").write("\n".join(lines) + "\n")


def changelog(path, version, date, notes_path):
    notes = open(notes_path, encoding="utf-8").read().strip()
    # nest the notes' own "## ..." headings under the release heading, like the existing entries
    notes = re.sub(r"(?m)^## ", "#### ", notes)
    section = f"## v{version} ({date})\n\n{notes}\n"

    content = open(path, encoding="utf-8").read()
    header = "# Changelog\n"
    if content.startswith(header):
        rest = content[len(header):].lstrip("\n")
        content = f"{header}\n\n{section}\n\n{rest}"
    else:
        content = f"{header}\n\n{section}\n\n{content}"
    open(path, "w", encoding="utf-8").write(content)


def inline_html(text):
    # `code` first, so nothing inside it becomes a link
    pieces = CODE.split(text)
    return "".join(f"<code>{html.escape(p, quote=False)}</code>" if i % 2 else inline_text(p) for i, p in enumerate(pieces))


def inline_text(text):
    # work on escaped text, then add markup for URLs, author @mentions and **bold**
    out = html.escape(text, quote=False)

    def link(match):
        url = match.group(0)
        pull = PULL.search(url)
        label = f"#{pull.group(1)}" if pull else url
        return f'<a href="{url}">{label}</a>'

    out = URL.sub(link, out)
    out = AUTHOR.sub(lambda m: m.group(0).replace(f"@{m.group(1)}", f'<a href="https://github.com/{m.group(1)}">@{m.group(1)}</a>'), out)
    return BOLD.sub(r"<b>\1</b>", out)


def to_html(notes):
    parts, in_list = [], False
    for line in notes.splitlines():
        stripped = line.strip()
        if stripped.startswith(("* ", "- ")):
            if not in_list:
                parts.append("<ul>")
                in_list = True
            parts.append(f"<li>{inline_html(stripped[2:])}</li>")
            continue
        if in_list:
            parts.append("</ul>")
            in_list = False
        if not stripped:
            continue
        heading = re.match(r"^#+\s+(.*)$", stripped)
        parts.append(f"<h3>{inline_html(heading.group(1))}</h3>" if heading else f"<p>{inline_html(stripped)}</p>")
    if in_list:
        parts.append("</ul>")
    return "\n".join(parts)


def change_notes(plugin_xml, notes_path, release_url):
    notes_html = to_html(open(notes_path, encoding="utf-8").read())
    notes_html += f'\n<p><a href="{html.escape(release_url)}">Release on GitHub</a></p>'
    content = open(plugin_xml, encoding="utf-8").read()
    if "CHANGELOG_PLACEHOLDER" not in content:
        raise SystemExit(f"CHANGELOG_PLACEHOLDER not found in {plugin_xml}")
    if "]]>" in notes_html:
        raise SystemExit("release notes contain ']]>', which would end the change-notes CDATA section")
    open(plugin_xml, "w", encoding="utf-8").write(content.replace("CHANGELOG_PLACEHOLDER", notes_html))


def main():
    command, args = (sys.argv[1], sys.argv[2:]) if len(sys.argv) > 1 else (None, [])
    if command == "normalize" and len(args) == 1:
        normalize(*args)
    elif command == "changelog" and len(args) == 4:
        changelog(*args)
    elif command == "change-notes" and len(args) == 3:
        change_notes(*args)
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
