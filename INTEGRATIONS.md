# Integrations

Start with the pinned-release setup in [`README.md`](README.md). The same
`.vale.ini` then works in Git hooks, editors, and AI-assisted rule development.

## Run Vale before commits with `prek`

[`prek`](https://prek.j178.dev/) runs standard pre-commit configurations, so
Vale's official [pre-commit configuration](https://docs.vale.sh/integrations/pre-commit)
works without the legacy `pre-commit` executable. Add
`.pre-commit-config.yaml` to the consumer repository:

```yaml
repos:
  - repo: https://github.com/vale-cli/vale
    rev: v3.18.0
    hooks:
      - id: vale
        name: vale sync
        pass_filenames: false
        args: [sync]
      - id: vale
        args: [--output=line, --minAlertLevel=suggestion]
```

The first hook installs the WriteSimply release pinned in `.vale.ini`. The
second checks staged files and fails on WriteSimply's suggestion-level alerts.
Install the Git hook, then check the whole repository once:

```bash
prek install
prek run --all-files
```

Keep `rev` pinned to a Vale release tag. Update it deliberately and rerun the
all-files check when upgrading Vale.

## See findings in an editor with Vale LSP

Install a supported editor client from the Vale LSP [editor
list](https://docs.vale.sh/guides/lsp#editors). Most clients start `vale-ls`
for you. If you configure a generic LSP client, use these initialization
options:

```json
{
  "initializationOptions": {
    "installVale": false,
    "syncOnStartup": true,
    "configPath": ""
  }
}
```

This setup uses `vale` from `PATH`, syncs the pinned WriteSimply package when
the server starts, and lets Vale find the nearest `.vale.ini`. Set
`valeBinaryPath` only when the editor cannot see the intended Vale binary.
The server reports findings while you type and offers quick fixes for
WriteSimply substitutions.

## Check AI-assisted changes with Vale MCP

Vale's hosted [MCP server](https://docs.vale.sh/guides/mcp) gives compatible AI
clients direct access to Vale's engine. Add the remote server to the client's
MCP configuration:

```json
{
  "mcpServers": {
    "vale-cms": {
      "type": "http",
      "url": "https://api.vale.sh/mcp"
    }
  }
}
```

Authenticate with a Vale CMS account as directed by the client. The hosted
server is a paid Vale CMS feature; the Vale CLI and WriteSimply remain free.

Ask the assistant to use `check_config` after editing `.vale.ini`, `lint_text`
to test sample prose, or `diff_style` before changing WriteSimply rules. These
tools verify generated changes against Vale's engine, but they do not replace
the repository test suite.
