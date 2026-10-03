# Adding to my DevOps notes

[Home](README.md) · [Topics](notes/README.md) · [Read later](LATEST.md)

## Daily workflow

1. Choose the closest topic in the [topic directory](notes/README.md). Use the [inbox](inbox/README.md) for an unfinished idea.
2. Create one note per concept. Use the helper below or copy [the note template](templates/note.md).
3. Record the useful takeaway, an example, sources, and what you actually tested.
4. Add a link to the topic's `README.md` and an unchecked entry at the top of [LATEST.md](LATEST.md). The helper does both for you.
5. When you have time to read, open `LATEST.md`, review an unchecked entry, and mark it `[x]`. Set the note's status to `reviewed` if it has one.

## Create a note with one command

Run from the repository root with Python 3.9+:

```bash
python3 scripts/new_note.py kubernetes/concepts "Pod disruption budgets"
python3 scripts/new_note.py github-actions "Reusable workflows"
python3 scripts/new_note.py linux "Systemd timers"
python3 scripts/new_note.py inbox "Read about OpenTelemetry"
```

The helper creates a template, adds a reading-list entry, and adds a link under **New notes** in the topic index. It uses today's local date, refuses to overwrite an existing note, and never commits changes. New subfolders within an existing topic are allowed.

## Add a note manually

1. Copy `templates/note.md` into a topic folder and replace the placeholders. Use `templates/lab.md` as `README.md` for a lab.
2. Add a relative link in that topic's `README.md`.
3. Add this line immediately below `<!-- entries -->` in `LATEST.md`, replacing the date, title, path, and summary:

```markdown
- [ ] YYYY-MM-DD — [Note title](notes/topic/note-title.md) — One sentence about what I added.
```

For an important update to an existing note, add a new unchecked entry labelled **Updated** with today's date. Small spelling fixes do not need an entry. `LATEST.md` is a curated log: edits made outside the helper must be logged manually.

## Where things belong

- Tool-specific concepts, commands, and troubleshooting go in `notes/<topic>/`.
- Keep a lab's code, manifests, and instructions together, such as `notes/kubernetes/nginx-demo/`.
- Put PDF course material in the topic's `assignments/` folder.
- Store screenshots beside the note in an `assets/` folder and link them relatively.
- Put cross-topic interview practice in `notes/interviews/`.
- File a note that spans topics once, under its main subject, then cross-link it elsewhere.
- For a new topic, create `notes/<topic>/README.md` describing its scope and link it from `notes/README.md` and the root README.

## Naming and maintenance

- Use lowercase names with hyphens: `remote-state-locking.md`. Keep standard names such as `README.md`, `Dockerfile`, and tool-required filenames.
- Use `YYYY-MM-DD-title.md` for inbox captures or dated learning sessions. Topic notes use descriptive names without a required date prefix.
- Use relative links so navigation works locally and on GitHub.
- Preserve original added dates; record a new date when substantially updating a note.
- Record versions and verification dates when behavior depends on the environment. Existing notes have not all been revalidated.
- Keep environments, generated state, credentials, and new database dumps out of Git. Commit requirements and example configuration instead.
- Run commands for a lab from the directory specified in its README.

## Before committing

```bash
git status --short
git diff --check
```

Check that your new links open and that `LATEST.md` includes any material you want to read later. Use a descriptive commit message such as `docs(kubernetes): add pod disruption budget notes`.
