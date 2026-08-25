# A New Kind of Science

This is the repository's canonical Markdown source for the complete book.
It contains 29 ordered book documents and their referenced figures:

- publication information and printed contents;
- Preface;
- Chapters 1–12;
- General Notes and Notes for Chapters 1–12;
- Index;
- Colophon.

Start with [Contents.md](Contents.md). The contents page is repository
navigation; the book text itself is contained in the linked documents.

Two generated reading aids are kept at the source root:

- [A-New-Kind-of-Science.md](A-New-Kind-of-Science.md) concatenates all 29
  canonical documents in reading order and rebases their local links.
- [ANKoS-Atlas.md](ANKoS-Atlas.md) maps the canonical documents and chapter
  sections back to their individual source files.

The 29 documents listed by `Contents.md` remain canonical. The combined source
and atlas are derived files and should be regenerated after canonical source
changes rather than edited independently.

Each chapter is stored in its own ordered directory under `CHAPTERS/`. The
chapter retains its full Markdown filename, and its referenced figures are
stored in the adjacent `images/` directory.

The notes documents follow the same layout under `BACK-MATTER/NOTES/`, with
source and component figures kept alongside each document in `images/`.
