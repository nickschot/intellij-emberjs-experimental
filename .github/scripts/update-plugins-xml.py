#!/usr/bin/env python3
"""
Writes the updatePlugins.xml of a custom JetBrains plugin repository for one built plugin zip.

The plugin's id, name, version, description, change notes and compatible build range are read from the
META-INF/plugin.xml inside the built zip, so they always match what is published.

Usage: update-plugins-xml.py <plugin.zip> <download-url>
"""
import io
import sys
import zipfile
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape, quoteattr


def plugin_descriptor(plugin_zip):
    with zipfile.ZipFile(plugin_zip) as outer:
        jars = [n for n in outer.namelist() if n.endswith(".jar") and "/lib/" in n]
        for jar in jars:
            with zipfile.ZipFile(io.BytesIO(outer.read(jar))) as inner:
                if "META-INF/plugin.xml" in inner.namelist():
                    return ET.fromstring(inner.read("META-INF/plugin.xml"))
    raise SystemExit(f"no META-INF/plugin.xml found in {plugin_zip}")


def main():
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    plugin_zip, url = sys.argv[1], sys.argv[2]
    descriptor = plugin_descriptor(plugin_zip)

    def text(tag):
        element = descriptor.find(tag)
        return (element.text or "").strip() if element is not None else ""

    plugin_id, version = text("id"), text("version")
    idea_version = descriptor.find("idea-version")
    if not plugin_id or not version or idea_version is None:
        raise SystemExit("plugin.xml is missing id, version or idea-version")

    since, until = idea_version.get("since-build"), idea_version.get("until-build")
    range_attrs = f"since-build={quoteattr(since)}" + (f" until-build={quoteattr(until)}" if until else "")

    print('<?xml version="1.0" encoding="UTF-8"?>')
    print("<plugins>")
    print(f"  <plugin id={quoteattr(plugin_id)} url={quoteattr(url)} version={quoteattr(version)}>")
    print(f"    <idea-version {range_attrs}/>")
    print(f"    <name>{escape(text('name'))}</name>")
    print(f"    <vendor>{escape(text('vendor'))}</vendor>")
    print(f"    <description><![CDATA[{text('description')}]]></description>")
    print(f"    <change-notes><![CDATA[{text('change-notes')}]]></change-notes>")
    print("  </plugin>")
    print("</plugins>")


if __name__ == "__main__":
    main()
