"""Foundation documentation contract; not runtime or governance certification."""
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
IDS = ("WT-PROJECT-OSINT-001", "WT-OSINT-CONTINUITY-20261125-01")
DOCS = ("README.md", "AGENTS.md", "SUIVI.md", "DECISIONS.md",
        "docs/foundations/AUTOMATION.md", "docs/foundations/LOOPS.md")
LINKS = DOCS[1:]
A_IDS = [f"A{i:02d}" for i in range(1, 19)]
L_IDS = [f"L{i:02d}" for i in range(1, 19)]
D_IDS = [f"D{i:02d}" for i in range(1, 9)]

def table_rows(text, prefix):
    return [line.split("|")[1:-1] for line in text.splitlines()
            if re.match(rf"^\|\s*{prefix}\d+\s*\|", line)]

def validate(root):
    errors, docs = [], {}
    for name in DOCS:
        path = root / name
        if not path.is_file():
            errors.append(f"missing: {name}")
            continue
        content = docs[name] = path.read_text(encoding="utf-8")
        for identifier in IDS:
            if identifier not in content:
                errors.append(f"{name}: missing {identifier}")
    readme = docs.get("README.md", "")
    for link in LINKS:
        if f"]({link})" not in readme:
            errors.append(f"README.md: missing link {link}")
    phase_section = readme.partition("## Fil conducteur de conception")[2].partition("\n## ")[0]
    phases = re.findall(r"^(\d+)\. ", phase_section, re.M)
    if phases != [str(i) for i in range(1, 20)]:
        errors.append("README.md: phase sequence must remain 1..19")
    for name, prefix, expected in (
        (DOCS[4], "A", A_IDS), (DOCS[5], "L", L_IDS), (DOCS[3], "D", D_IDS)
    ):
        rows = table_rows(docs.get(name, ""), prefix)
        if [row[0].strip() for row in rows] != expected:
            errors.append(f"{name}: missing, duplicated or reordered IDs")
    used = set()
    for row in table_rows(docs.get(DOCS[5], ""), "L"):
        if len(row) != 5:
            errors.append("LOOPS.md: malformed loop row")
            continue
        refs = set(row[3].split())
        if not refs or not refs <= set(A_IDS):
            errors.append(f"LOOPS.md: invalid socles in {row[0].strip()}")
        used.update(refs)
    if not set(A_IDS) <= used:
        errors.append("LOOPS.md: uncovered socles")
    for row in table_rows(docs.get(DOCS[3], ""), "D"):
        if len(row) != 4 or row[2].strip() not in {"OPEN", "CONFIRMED", "SUPERSEDED"}:
            errors.append("DECISIONS.md: invalid decision row")
    return errors

class ContractTests(unittest.TestCase):
    def setUp(self):
        from tempfile import TemporaryDirectory
        tmp = TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        for name in DOCS:
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text((ROOT / name).read_text(encoding="utf-8"), encoding="utf-8")
    def change(self, name, old, new):
        path = self.root / name
        original = path.read_text(encoding="utf-8")
        self.assertIn(old, original)
        path.write_text(original.replace(old, new, 1), encoding="utf-8")
    def test_valid(self):
        self.assertEqual(validate(self.root), [])
    def test_missing_doc(self):
        (self.root / "SUIVI.md").unlink()
        self.assertIn("missing: SUIVI.md", validate(self.root))
    def test_wrong_id(self):
        self.change("AGENTS.md", IDS[1], "WRONG")
        self.assertTrue(any("AGENTS.md: missing" in e for e in validate(self.root)))
    def test_missing_link(self):
        self.change("README.md", "](DECISIONS.md)", "](missing.md)")
        self.assertIn("README.md: missing link DECISIONS.md", validate(self.root))
    def test_phase_drift(self):
        self.change("README.md", "19. ", "20. ")
        self.assertTrue(any("phase sequence" in e for e in validate(self.root)))
    def test_duplicate_socle(self):
        self.change(DOCS[4], "| A02 |", "| A01 |")
        self.assertTrue(any("duplicated" in e for e in validate(self.root)))
    def test_unknown_socle(self):
        self.change(DOCS[5], "A01 A02 A06", "A99 A02 A06")
        self.assertTrue(any("invalid socles" in e for e in validate(self.root)))
    def test_duplicate_loop(self):
        self.change(DOCS[5], "| L02 |", "| L01 |")
        self.assertTrue(any("duplicated" in e for e in validate(self.root)))
    def test_invalid_decision(self):
        self.change("DECISIONS.md", "| OPEN |", "| UNKNOWN |")
        self.assertIn("DECISIONS.md: invalid decision row", validate(self.root))

if __name__ == "__main__":
    errors = validate(ROOT)
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        sys.exit(1)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(ContractTests)
    tests = unittest.TextTestRunner(verbosity=2).run(suite)
    if not tests.wasSuccessful():
        sys.exit(1)
    print("PASS: foundation documentation contract (not runtime certification)")
