# WriteSimply

WriteSimply is a small [Vale](https://vale.sh/) style for direct prose. It
flags wordy substitutions, empty framing, and sentences longer than 30 words.
The package is tested with Vale 3.18.0 against Markdown and MDX.

## Inspiration and limits

The style is explicitly inspired by Paul Graham's essay
[“Write Simply”](https://paulgraham.com/simply.html), especially its aim to
use “ordinary words and simple sentences.” The package turns only narrow,
observable patterns into alerts. Graham did not author or endorse these
rules.

Vale can match phrases, substitutions, counts, document-level metrics, and
part-of-speech sequences. Its official documentation describes the available
[checks](https://docs.vale.sh/topics/styles), including
[substitution](https://docs.vale.sh/checks/substitution),
[metric](https://docs.vale.sh/checks/metric), and
[sequence](https://docs.vale.sh/checks/sequence). Capability alone does not
make a check useful. Each enabled rule must point to a specific edit without
guessing at the writer's purpose.

### Candidate review

- **Ordinary words: already covered.** `PlainWords` gives exact replacements
  for 14 bureaucratic forms. A broad “fancy words” list would duplicate that
  purpose while flagging precise domain terms. Benefit: lower reading effort.
  Limitation: simple and precise are contextual. False-positive risk becomes
  high beyond the reviewed phrase list, so no broad vocabulary rule was added.
- **Simple sentences: already covered.** `SentenceLength` supplies an
  objective 30-word editing prompt. Benefit: it finds sentences worth
  rereading. Limitation: length is not syntactic complexity. False-positive
  risk remains in readable technical sentences, so the alert stays a
  suggestion and the threshold is unchanged.
- **Direct verbs: enabled.** `DirectVerbs` turns three exact wordy
  constructions into shorter verbs and handles their common inflections.
  Benefit: fewer words with the same meaning. Limitation: it does not detect
  nominalizations generally. False-positive risk is low, but a writer may
  retain a construction for deliberate cadence or emphasis.
- **Categorical redundancy: enabled.** `Redundancy` removes a modifier from
  four phrases where the noun already carries it. Benefit: safe cutting with
  a concrete replacement. Limitation: the list is intentionally small.
  False-positive risk is low but not zero when repetition is deliberate.
- **Readability scores: rejected.** Vale's `metric` check can calculate a
  document-level score, but it would overlap the existing word and sentence
  rules and penalize necessary technical names. The score gives no reliable
  local edit and has high false-positive risk on short or scientific files.
- **Passive voice and broad nominalizations: rejected.** Vale's `sequence`
  check can inspect parts of speech, but these forms are often appropriate in
  methods, incident reports, and API documentation. The expected volume and
  parser ambiguity outweigh the possible benefit.
- **Acronyms and idioms: rejected.** Explaining unfamiliar language can help
  non-native readers, but familiarity depends on audience and definitions may
  live elsewhere in a documentation set. A universal package would need a
  large, consumer-specific exception list.

Weak ideas, honesty, intentional complexity, durability, and whether prose is
trying to impress are editorial judgments, not properties Vale can determine.
Writers should use those principles during review, along with deliberate
exceptions for effect. Possible future guidance, rather than enabled checks,
includes reviewing idioms for international readers, cutting throat-clearing
openings, preferring concrete subjects, and testing whether every paragraph
advances the idea.

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

See the [integrations guide](INTEGRATIONS.md) to run WriteSimply before commits
with `prek`, show findings in editors through Vale LSP, or check AI-assisted
changes through Vale MCP.

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
- `WriteSimply.DirectVerbs` replaces three wordy verb constructions and their
  common inflections: `make use of`, `take into consideration`, and `give
  consideration to`. Exact phrases keep the alert precise; the rule does not
  attempt to identify nominalizations in general.
- `WriteSimply.Redundancy` removes one word from four categorical phrases,
  including `added bonus` and `completely unanimous`. It intentionally omits
  context-sensitive repetitions such as `end result` and `future plans`.

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
├── DirectVerbs.yml
├── Filler.yml
├── PlainWords.yml
├── Redundancy.yml
├── SentenceLength.yml
└── meta.json
```

`scripts/package.py` creates `WriteSimply.zip` with that directory at the
archive root, which is the layout `vale sync` expects. `tests/test.py` builds
the archive twice and requires byte-identical output. It installs the archive
into a temporary consumer with `vale sync`, compares the installed files byte
for byte, checks exact fixture results, and lints this project's Markdown with
the installed package.

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

After the first approved release, follow [`DISCOVERY.md`](DISCOVERY.md) to add
the GitHub topic and prepare the Vale Package Explorer catalog pull request.

## Provenance and license

[`PROVENANCE.md`](PROVENANCE.md) records the supplied archive checksum, source
commit, original path, and the one reviewed correction to the canonical
rules.

WriteSimply is available under the [MIT License](LICENSE).
