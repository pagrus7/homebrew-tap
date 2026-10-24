# Kaferry Homebrew tap

Install the published Kaferry release on macOS or Linux (ARM64 or AMD64):

```sh
brew install pagrus7/tap/kaferry
kaferry --version
```

The formula downloads Kaferry's release archive without compiling it. Homebrew verifies its pinned SHA-256 checksum. The installed `share/kaferry` directory contains `LICENSE` and `THIRD_PARTY_NOTICES.txt`. Run `kaferry --version`, then select the matching release's documentation from the [releases list](https://github.com/pagrus7/kaferry/releases).

## Updating the formula

Prerequisites: Python 3, GitHub CLI with repository read access, and a published stable Kaferry release. From this checkout:

```sh
python3 scripts/update_formula.py vX.Y.Z
```

The generator resolves the exact tag commit, downloads all four archives, checks their checksums and required files, and verifies GitHub provenance against Kaferry's release workflow, tag and commit. It writes `Formula/kaferry.rb` only after every archive passes. Review and commit the formula change in a PR; the script does not push or merge. Published tags and archives stay unchanged.

CI repeats verification, then audits, installs and tests the formula on all four native targets. It verifies the exact version/commit and installed license files. Local checks:

```sh
python3 -m unittest discover -s scripts -p 'test_*.py'
python3 scripts/update_formula.py vX.Y.Z --check
brew audit --strict pagrus7/tap/kaferry
brew test pagrus7/tap/kaferry
```
