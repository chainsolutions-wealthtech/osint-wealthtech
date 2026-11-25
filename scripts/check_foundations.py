"""Minimal documentation contract; no application or network dependency."""
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
IDS = ("WT-PROJECT-OSINT-001", "WT-OSINT-CONTINUITY-20261125-01")
DOCS = ("README.md", "AGENTS.md", "SUIVI.md", "docs/foundations/AUTOMATION.md")
LINKS = ("AGENTS.md", "SUIVI.md", "docs/foundations/AUTOMATION.md")

def validate(root):
    errors = []
    for name in DOCS:
        path = root / name
        if not path.is_file():
            errors.append(f"missing: {name}")
            continue
        content = path.read_text(encoding="utf-8")
        for identifier in IDS:
            if identifier not in content:
                errors.append(f"{name}: missing {identifier}")
        if name == "README.md":
            for link in LINKS:
                if f"]({link})" not in content:
                    errors.append(f"README.md: missing link {link}")
    return errors

class ContractTests(unittest.TestCase):
    def test_valid_and_negative_cases(self):
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in DOCS:
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(" ".join(IDS) + "\n" + "\n".join(f"[doc]({x})" for x in LINKS), encoding="utf-8")
            self.assertEqual(validate(root), [])
            (root / "AGENTS.md").write_text(IDS[0], encoding="utf-8")
            self.assertTrue(any("AGENTS.md: missing" in x for x in validate(root)))
            (root / "SUIVI.md").unlink()
            self.assertIn("missing: SUIVI.md", validate(root))
            (root / "README.md").write_text(" ".join(IDS), encoding="utf-8")
            self.assertTrue(any("missing link" in x for x in validate(root)))

if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ContractTests)
    tests = unittest.TextTestRunner(verbosity=2).run(suite)
    errors = validate(ROOT)
    for error in errors:
        print(error, file=sys.stderr)
    if not tests.wasSuccessful() or errors:
        sys.exit(1)
    print("PASS: minimal documentation contract (not runtime certification)")
