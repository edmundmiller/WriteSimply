# Provenance

WriteSimply comes from the `WriteSimply` Vale package in the user-supplied
`nascent-manuscript-main` source archive.

- Archive: `nascent-manuscript-main.zip`
- Archive SHA-256: `275a49bfef61794e2dce5e8ea25d0be802e1597050c32df8b4f83cb0c28e4f86`
- Archived Git commit: `ca9b2a5b446fe3f9c3b78cfa75c8e595615c4643`
- Source path: `.vale/packages/WriteSimply/WriteSimply`
- Extracted on: 2026-08-24

The package originally contained `PlainWords.yml`, `Filler.yml`, and
`SentenceLength.yml`. The Git history adds each source rule separately so
that reviews can trace any corrections and tests back to the archive.

## Reviewed differences

All source phrases, matching behavior, alert levels, and the 30-word threshold
are preserved. One replacement was corrected: `a majority of` suggested
`most` in the archive, which produced ungrammatical text such as `most the
samples`; the package suggests `most of` instead.
