#!/usr/bin/env python3
"""Create a learning note and link it from the reading queue and topic index."""

import argparse
from datetime import date
from pathlib import Path
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
MARKER = '<!-- entries -->'
INDEX_MARKER = '<!-- new-notes -->'


def markdown_text(text):
    """Escape characters that could break a Markdown link label."""
    return re.sub(r'([\\`*_[\]<>])', r'\\\1', text)


def create_note(root, destination, title, today=None):
    today = today or date.today().isoformat()
    title = title.strip()
    if not title or any(ord(char) < 32 or ord(char) == 127 for char in title):
        raise ValueError('Use a nonempty, single-line title.')
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*(?:/[a-z0-9]+(?:-[a-z0-9]+)*)*', destination):
        raise ValueError('Use a topic/subfolder path with lowercase letters, numbers, and hyphens.')
    topic = destination.split('/')[0]
    if topic == 'inbox' and destination != 'inbox':
        raise ValueError('Use inbox without a subfolder.')
    base = root / 'inbox' if topic == 'inbox' else root / 'notes' / topic
    if not (base / 'README.md').is_file():
        raise ValueError(f'Unknown topic: {topic}. Choose a topic from notes/README.md or use inbox.')
    folder = root / 'inbox' if topic == 'inbox' else root / 'notes' / destination
    # Resolve symlinks before writing, too.
    if not folder.resolve().is_relative_to(root.resolve()):
        raise ValueError('The destination must stay inside this repository.')
    ascii_title = unicodedata.normalize('NFKD', title).encode('ascii', 'ignore').decode()
    slug = re.sub(r'[^a-z0-9]+', '-', ascii_title.lower()).strip('-')
    if not slug:
        raise ValueError('Include at least one Latin letter or number in the title for the filename.')
    if topic == 'inbox':
        slug = today + '-' + slug
    path = folder / (slug + '.md')
    if path.exists() or path.is_symlink():
        raise ValueError(f'Note already exists: {path.relative_to(root)}. Update it and log the change manually.')
    latest = root / 'LATEST.md'
    log = latest.read_text(encoding='utf-8')
    if log.count(MARKER) != 1:
        raise ValueError('LATEST.md must contain exactly one <!-- entries --> marker.')
    template = (root / 'templates/note.md').read_text(encoding='utf-8')
    values = {'title': markdown_text(title), 'date': today, 'topic': destination}
    content = re.sub(r'\{\{(title|date|topic)\}\}', lambda match: values[match[1]], template)
    relative = path.relative_to(root).as_posix()
    entry = f'- [ ] {today} — [{markdown_text(title)}]({relative}) — Added for review.'
    index = base / 'README.md'
    index_text = index.read_text(encoding='utf-8')
    if topic != 'inbox':
        if INDEX_MARKER not in index_text:
            index_text = index_text.rstrip() + '\n\n## New notes\n\n' + INDEX_MARKER + '\n'
        link = f'- [{markdown_text(title)}]({path.relative_to(base).as_posix()})'
        index_text = index_text.replace(INDEX_MARKER, INDEX_MARKER + '\n' + link, 1)
    folder.mkdir(parents=True, exist_ok=True)
    # Exclusive creation avoids overwriting a note created between the checks.
    with path.open('x', encoding='utf-8') as handle:
        handle.write(content)
    latest.write_text(log.replace(MARKER, MARKER + '\n' + entry, 1), encoding='utf-8')
    if topic != 'inbox':
        index.write_text(index_text, encoding='utf-8')
    return relative


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', help='Existing topic, topic/subfolder, or inbox')
    parser.add_argument('title', help='Note title, in quotes')
    args = parser.parse_args()
    try:
        path = create_note(ROOT, args.destination, args.title)
    except (ValueError, OSError) as error:
        parser.exit(1, f'Error: {error}\n')
    print(f'Created {path}\nAdded to LATEST.md. Fill in your note, then review it when ready.')


if __name__ == '__main__':
    main()
