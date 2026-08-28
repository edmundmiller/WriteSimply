# Changelog

## Unreleased

### Changed

- Raised the `SentenceLength` threshold from 30 to 35 words to focus findings
  on sentences more likely to need editorial revision.

## 1.0.0 - 2026-08-26

### Added

- `WriteSimply.DirectVerbs`, with exact substitutions for inflections of
  `make use of`, `take into consideration`, and `give consideration to`.
- `WriteSimply.Redundancy`, with four low-ambiguity redundant phrases.
- Attribution to Paul Graham's “Write Simply” and documented boundaries for
  principles that require human editorial judgment.

The new rules add suggestion-level alerts. Existing `PlainWords`, `Filler`,
and 30-word `SentenceLength` behavior is unchanged.
