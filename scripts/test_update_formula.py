"""A formula update accepts only intact archives and retains redistribution files."""

import hashlib
import io
from pathlib import Path
import tarfile
import tempfile
import unittest

from update_formula import archive_digest, formula


class FormulaTest(unittest.TestCase):
    def test_corrupt_or_duplicate_checksum_fails(self):
        # Given an archive and its recorded hash.
        with tempfile.TemporaryDirectory() as name:
            path = Path(name) / 'archive.tar.gz'
            with tarfile.open(path, 'w:gz') as archive:
                for filename in ('kaferry', 'LICENSE', 'THIRD_PARTY_NOTICES.txt'):
                    info = tarfile.TarInfo(filename)
                    info.size = 1
                    archive.addfile(info, io.BytesIO(b'x'))
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            row = f'{digest}  {path.name}\n'
            # When verifying intact bytes, then retain their hash.
            self.assertEqual(archive_digest(path, row), digest)
            # When checksums are absent, duplicated or wrong, then reject the archive.
            for checksums in ('', row + row, '0' * 64 + f'  {path.name}\n'):
                with self.subTest(checksums=checksums), self.assertRaises(ValueError):
                    archive_digest(path, checksums)

    def test_missing_license_or_link_member_fails(self):
        # Given signed but incorrectly packaged contents, even with matching checksums.
        with tempfile.TemporaryDirectory() as name:
            path = Path(name) / 'archive.tar.gz'
            for files in [('kaferry',), ('kaferry', 'LICENSE', '../THIRD_PARTY_NOTICES.txt')]:
                with tarfile.open(path, 'w:gz') as archive:
                    for filename in files:
                        info = tarfile.TarInfo(filename)
                        info.size = 1
                        archive.addfile(info, io.BytesIO(b'x'))
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
                # When checking the archive layout, then reject incomplete/unsafe packages.
                with self.subTest(files=files), self.assertRaises(ValueError):
                    archive_digest(path, f'{digest}  {path.name}\n')

    def test_all_platforms_and_licenses_are_installed(self):
        # Given distinct checksums for the four supported archive targets.
        hashes = {'darwin-arm64': 'a' * 64, 'darwin-amd64': 'b' * 64,
                  'linux-arm64': 'c' * 64, 'linux-amd64': 'd' * 64}
        # When generating a formula, then bind every URL to its checksum and exact build.
        text = formula('v1.2.3', 'e' * 40, hashes)
        for platform, digest in hashes.items():
            self.assertIn(f'kaferry-v1.2.3-{platform}.tar.gz"\n      sha256 "{digest}"', text)
        self.assertIn('pkgshare.install "LICENSE", "THIRD_PARTY_NOTICES.txt"', text)
        self.assertIn('kaferry v1.2.3 (commit ' + 'e' * 40, text)


if __name__ == '__main__':
    unittest.main()
