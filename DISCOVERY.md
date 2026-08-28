# Discovery checklist

These steps make WriteSimply easier to find after its first approved release.
They change external project state, so a maintainer must perform them manually.

## Release prerequisite

The Vale Package Explorer requires a working release asset URL. Before opening
a catalog pull request:

1. Review and merge the intended release commits.
2. Move the relevant `CHANGELOG.md` entries from `Unreleased` to the approved
   semantic version and date.
3. Run the release checks from `README.md` at the commit to tag.
4. With explicit approval, create and push the tag, then publish the generated
   archive as an asset named `WriteSimply.zip`.
5. Confirm that the archive contains one top-level `WriteSimply/` directory and
   that this URL downloads it:

   ```text
   https://github.com/edmundmiller/WriteSimply/releases/latest/download/WriteSimply.zip
   ```

Release `v1.0.0` and its `WriteSimply.zip` asset are available. The working
release asset is the exact prerequisite for catalog submission. Choose future
versions from the release policy in `README.md`; do not create a version only
to satisfy the catalog.

## GitHub discovery

In the repository settings, add this description:

> A small Vale style for direct prose.

Add the `vale-linter-style` topic. This places the repository in Vale's
[community topic listing](https://github.com/topics/vale-linter-style), but it
does not add the package to the curated Package Explorer.

## Vale Package Explorer

After the release prerequisite passes, fork
[`vale-cli/packages`](https://github.com/vale-cli/packages). Add this entry to
`library.json` in alphabetical order, then open a pull request:

```json
{
    "name": "WriteSimply",
    "description": "Flags wordy substitutions, empty framing, and long sentences.",
    "homepage": "https://github.com/edmundmiller/WriteSimply",
    "url": "https://github.com/edmundmiller/WriteSimply/releases/latest/download/WriteSimply.zip",
    "tags": [
        "style"
    ]
}
```

The catalog checks the JSON keys, ordering, URLs, archive structure, and Vale
rule loading. A merged catalog entry makes `Packages = WriteSimply` available
and adds the package to the [Vale Package Explorer](https://vale.sh/explorer).
Consumers that need reproducible results should still use the versioned
release URL shown in `README.md`.
