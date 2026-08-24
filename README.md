# WriteSimply

WriteSimply is a small [Vale](https://vale.sh/) style for direct prose. It
flags wordy substitutions, empty framing, and sentences longer than 30 words.
The package is tested with Vale 3.18.0 against Markdown and MDX.

## Install a pinned release

Add a release URL to the consumer repository's `.vale.ini`:

```ini
StylesPath = .vale/styles
MinAlertLevel = suggestion
Packages = https://github.com/edmundmiller/write-simply/releases/download/v1.0.0/WriteSimply.zip

IgnoredScopes = code, tt, img, url, a
SkippedScopes = script, style, pre, figure, code

[*.{md,mdx}]
BasedOnStyles = WriteSimply
```

Then install the package and lint the prose:

```bash
vale sync
vale README.md docs/
```

Commit `.vale.ini`, but ignore the generated `.vale/styles/` directory. Use
the tagged release URL rather than a `latest` URL so rule updates cannot
change consumer results unexpectedly.

The same configuration works in `edmundmiller.dev` and
`nascent-manuscript`. Each repository should keep its own formats, vocabulary,
and local rules, then add `WriteSimply` to the applicable `BasedOnStyles`
list. For LaTeX treated as Markdown, for example:

```ini
[formats]
tex = md

[*.tex]
BasedOnStyles = WriteSimply
```

## Rules

- `WriteSimply.PlainWords` suggests shorter replacements for 14 bureaucratic
  words and phrases. This includes `utilization`, which can be a precise term
  in scientific or systems writing; keep it when the technical meaning is
  intentional.
- `WriteSimply.Filler` flags five empty lead-ins, including `it is worth
  noting that` and `needless to say`.
- `WriteSimply.SentenceLength` suggests splitting sentences with more than
  30 `\w+` tokens. The rule counts hyphenated terms as multiple tokens and
  numbers as tokens, matching the canonical source behavior.

All findings are suggestions. Vale's markup parser, together with the
`IgnoredScopes` and `SkippedScopes` settings above, excludes inline code,
fenced code, HTML code elements, links, and MDX component attributes. Prose
outside those scopes remains linted.

Consumers can override a rule after `BasedOnStyles` when its tradeoff does not
fit their corpus:

```ini
WriteSimply.PlainWords = NO
```

## Package layout

`WriteSimply/` is the style-only package root:

```text
WriteSimply/
├── Filler.yml
├── PlainWords.yml
├── SentenceLength.yml
└── meta.json
```

`scripts/package.py` creates `WriteSimply.zip` with that directory at the
archive root, which is the layout `vale sync` expects. `tests/test.py` builds
the archive, installs it into a temporary consumer with `vale sync`, compares
the installed files byte for byte, and checks exact positive and negative
fixture results.

## Develop and test

The project pins Vale in `.vale-version`. In an Amp orb, or on Debian with
the standard command-line tools, prepare the environment and run the suite:

```bash
.agents/setup
VALE="$HOME/.local/bin/vale" python3 tests/test.py
python3 scripts/package.py dist/WriteSimply.zip
```

`.agents/setup` installs only missing prerequisites and a checksum-verified
Vale binary. `.agents/resume` performs a fast, non-destructive version check
when an orb wakes. Verify both lifecycle scripts with:

```bash
.agents/setup
.agents/setup                 # warm idempotence check
.agents/resume
env -i HOME="$HOME" PATH=/usr/local/bin:/usr/bin:/bin \
  /bin/bash -lc 'cd "$PWD" && .agents/resume'
```

Run the test suite after changing any rule or fixture. CI executes the same
setup, archive-install, and fixture flow on every pull request and push to
`main`.

## Version and release

Use semantic versions and keep consumers pinned:

- Major: remove or rename rules, or change established rule meaning.
- Minor: add rules or matches that can produce new alerts.
- Patch: fixes and metadata, test, or documentation changes that do not add
  alerts for previously clean prose.

To prepare a release after review, run the tests, build the archive, and record
its digest:

```bash
VALE="$HOME/.local/bin/vale" python3 tests/test.py
python3 scripts/package.py dist/WriteSimply.zip
sha256sum dist/WriteSimply.zip
```

Create an annotated tag such as `v1.0.0`, push it only with approval, and
publish `dist/WriteSimply.zip` as the release asset. Consumers can then replace
the example URL with that exact tag. A version bump means changing the pinned
URL and running `vale sync` again.

## Provenance and license

[`PROVENANCE.md`](PROVENANCE.md) records the supplied archive checksum, source
commit, original path, and the one reviewed correction to the canonical
rules.

WriteSimply is available under the [MIT License](LICENSE).
