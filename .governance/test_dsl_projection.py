"""Regression checks for target-owned, lock-derived package ownership."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from render_dsl_manifest import OUTPUT, SOURCE, project, render


class ProjectionTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / ".governance").mkdir()
        (self.root / SOURCE).write_text("{}\n")
        self.lock = {"schema": "new-project.lock/v1", "standard": {
            "id": "wellmanifest/new-project", "sourceRepository": "wellmanifest/new-project",
            "sourceRevision": "a" * 40, "version": "0.20.29", "publicationStatus": "published"},
            "managedFiles": {SOURCE: hashlib.sha256(b"{}\n").hexdigest()}}
        self.save_lock()

    def save_lock(self):
        (self.root / ".governance/manifest.lock.json").write_text(json.dumps(self.lock))

    def test_deterministic_and_read_only_check(self):
        render(self.root)
        before = (self.root / OUTPUT).read_bytes()
        render(self.root, check=True)
        self.assertEqual(before, (self.root / OUTPUT).read_bytes())
        self.assertEqual([OUTPUT, SOURCE], project(self.root)["ownedPaths"])

    def test_managed_drift_rejected_without_repairing_lock(self):
        (self.root / SOURCE).write_text("changed")
        with self.assertRaisesRegex(ValueError, "digest mismatch"):
            render(self.root)
        self.assertFalse((self.root / OUTPUT).exists())

    def test_stale_projection_rejected(self):
        render(self.root)
        self.lock["standard"]["sourceRevision"] = "b" * 40
        self.save_lock()
        with self.assertRaisesRegex(ValueError, "stale"):
            render(self.root, check=True)

    def test_new_managed_contract_is_projected_automatically(self):
        name = ".governance/new-contract.schema.json"
        (self.root / name).write_text("[]\n")
        self.lock["managedFiles"][name] = hashlib.sha256(b"[]\n").hexdigest()
        self.save_lock()
        self.assertIn(name, project(self.root)["ownedPaths"])
        self.assertNotIn("schemas/deployment.schema.json", project(self.root)["ownedPaths"])

    def test_unpublished_pin_rejected(self):
        self.lock["standard"]["publicationStatus"] = "unpublished-test"
        self.save_lock()
        with self.assertRaisesRegex(ValueError, "published"):
            project(self.root)

    def test_unsafe_managed_path_rejected(self):
        for name in ("../outside", "/outside", "dir\\outside"):
            with self.subTest(name=name):
                self.lock["managedFiles"] = {SOURCE: hashlib.sha256(b"{}\n").hexdigest(), name: "a" * 64}
                self.save_lock()
                with self.assertRaisesRegex(ValueError, "unsafe"):
                    project(self.root)

    def test_symlink_output_rejected(self):
        try:
            (self.root / OUTPUT).symlink_to(self.root / SOURCE)
        except OSError:
            self.skipTest("symlink creation unavailable")
        with self.assertRaisesRegex(ValueError, "symlink"):
            render(self.root)

    def test_real_adopted_package(self):
        root = Path(__file__).resolve().parents[1]
        render(root, check=True)


if __name__ == "__main__":
    unittest.main()
