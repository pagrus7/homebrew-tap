"""Generate the formula from checksum- and provenance-verified release archives."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tarfile
import tempfile


REPO = "pagrus7/kaferry"
PLATFORMS = ("darwin-arm64", "darwin-amd64", "linux-arm64", "linux-amd64")


def revision(tag):
    item = json.loads(subprocess.check_output(["gh", "api", f"repos/{REPO}/git/ref/tags/{tag}"], text=True))["object"]
    while item["type"] == "tag":
        item = json.loads(subprocess.check_output(["gh", "api", f"repos/{REPO}/git/tags/{item['sha']}"], text=True))["object"]
    if item["type"] != "commit" or not re.fullmatch("[a-f0-9]{40}", item["sha"]):
        raise ValueError("release tag must resolve to a commit")
    return item["sha"]


def archive_digest(path, checksums):
    matches = re.findall(r"^([a-f0-9]{64})  " + re.escape(path.name) + r"$", checksums, re.M)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if matches != [digest]:
        raise ValueError(f"missing, duplicate or incorrect checksum: {path.name}")
    with tarfile.open(path) as archive:
        members = archive.getmembers()
        if sorted(member.name for member in members) != ["LICENSE", "THIRD_PARTY_NOTICES.txt", "kaferry"] or not all(member.isfile() and member.size for member in members):
            raise ValueError("archive must contain the binary and nonempty license/notice files")
    return digest


def formula(tag, commit, hashes):
    blocks = []
    for system, prefix in (("macos", "darwin"), ("linux", "linux")):
        lines = [f"  on_{system} do"]
        for cpu, architecture in (("arm", "arm64"), ("intel", "amd64")):
            name = f"kaferry-{tag}-{prefix}-{architecture}.tar.gz"
            lines += [f"    on_{cpu} do", f'      url "https://github.com/{REPO}/releases/download/{tag}/{name}"',
                      f'      sha256 "{hashes[prefix + "-" + architecture]}"', "    end"]
        blocks += lines + ["  end", ""]
    return '\n'.join([
        "class Kaferry < Formula", '  desc "Copy Kafka records and Avro archives with SQL"',
        f'  homepage "https://github.com/{REPO}"', f'  version "{tag[1:]}"', '  license "MIT"', "",
        *blocks, "  def install", '    bin.install "kaferry"',
        '    pkgshare.install "LICENSE", "THIRD_PARTY_NOTICES.txt"', "  end", "", "  test do",
        '    output = shell_output("#{bin}/kaferry --version")',
        f'    assert_match "kaferry {tag} (commit {commit}; ", output',
        '    assert_match "MIT License", (pkgshare/"LICENSE").read',
        '    assert_match "Go runtime and standard library", (pkgshare/"THIRD_PARTY_NOTICES.txt").read',
        "  end", "end", "",
    ])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("tag", help="published stable release, such as v0.5.0")
    parser.add_argument("--check", action="store_true", help="compare without changing the formula")
    args = parser.parse_args()
    if not re.fullmatch(r"v[0-9]+\.[0-9]+\.[0-9]+", args.tag):
        parser.error("expected a stable version tag")
    release = json.loads(subprocess.check_output(["gh", "release", "view", args.tag, "--repo", REPO,
                                                "--json", "tagName,isDraft,isPrerelease"], text=True))
    if release != {"tagName": args.tag, "isDraft": False, "isPrerelease": False}:
        raise ValueError("formula requires a published stable release")
    commit = revision(args.tag)
    with tempfile.TemporaryDirectory(prefix="kaferry-formula-") as name:
        directory = Path(name)
        subprocess.run(["gh", "release", "download", args.tag, "--repo", REPO, "--dir", name,
                        "--pattern", "SHA256SUMS", "--pattern", "provenance-*.json", "--pattern", f"kaferry-{args.tag}-*.tar.gz"], check=True)
        checksums = (directory / "SHA256SUMS").read_text()
        hashes = {}
        for platform in PLATFORMS:
            path = directory / f"kaferry-{args.tag}-{platform}.tar.gz"
            hashes[platform] = archive_digest(path, checksums)
            subprocess.run(["gh", "attestation", "verify", str(path), "--repo", REPO,
                            "--bundle", str(directory / f"provenance-{platform}.json"),
                            "--signer-workflow", f"{REPO}/.github/workflows/release.yml",
                            "--source-ref", f"refs/tags/{args.tag}", "--source-digest", commit,
                            "--deny-self-hosted-runners"], check=True)
        text = formula(args.tag, commit, hashes)
    target = Path(__file__).resolve().parent.parent / "Formula/kaferry.rb"
    if args.check:
        if target.read_text() != text:
            raise ValueError("formula differs from the verified release; regenerate and review the change")
    else:
        target.write_text(text)
    print(f"Formula verified against {args.tag} ({commit})")


if __name__ == "__main__":
    main()
