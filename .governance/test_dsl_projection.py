"""Regression checks for target-owned, lock-derived package ownership."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile
import textwrap
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


class ChangeBoundaryTest(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parents[1]
        workflow = (self.root / ".github/workflows/ci.yml").read_text()
        step = workflow.split("      - name: Resolve exact change boundary\n", 1)[1]
        step = step.split("      - name:", 1)[0]
        self.command = textwrap.dedent(step.split("        run: |\n", 1)[1])
        self.head = self.git("HEAD")
        self.base = self.git("refs/remotes/origin/main")

    def git(self, ref):
        return subprocess.check_output(["git", "rev-parse", ref], cwd=self.root, text=True).strip()

    def run_boundary(self, event, ref, before, head=None):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "output"
            env = {**os.environ, "EVENT_NAME": event, "REF_NAME": ref,
                   "DEFAULT_BRANCH": "main", "EVENT_BASE_SHA": before,
                   "EVENT_HEAD_SHA": head or self.head, "GITHUB_OUTPUT": str(output)}
            result = subprocess.run(["bash", "-c", self.command], cwd=self.root,
                                    env=env, capture_output=True, text=True)
            values = dict(line.split("=", 1) for line in output.read_text().splitlines()) if output.exists() else {}
            return result.returncode, values

    def test_followup_push_uses_integration_base_not_previous_ticket_head(self):
        code, output = self.run_boundary("push", "ticket/009-atomic-governance-adoption", self.head)
        self.assertEqual(0, code)
        self.assertEqual(self.base, output["base"])
        self.assertEqual("range", output["mode"])

    def test_pull_request_preserves_exact_event_base(self):
        code, output = self.run_boundary("pull_request", "13/merge", self.base)
        self.assertEqual(0, code)
        self.assertEqual(self.base, output["base"])

    def test_default_branch_uses_repository_mode(self):
        code, output = self.run_boundary("push", "main", "0" * 40)
        self.assertEqual(0, code)
        self.assertEqual("repository", output["mode"])

    def test_manual_ticket_run_uses_integration_base(self):
        code, output = self.run_boundary("workflow_dispatch", "ticket/009-atomic-governance-adoption", "")
        self.assertEqual(0, code)
        self.assertEqual(self.base, output["base"])

    def test_missing_pr_base_and_invalid_head_fail_closed(self):
        for before, head in (("", self.head), (self.base, "invalid")):
            with self.subTest(before=before, head=head):
                code, _ = self.run_boundary("pull_request", "13/merge", before, head)
                self.assertNotEqual(0, code)


if __name__ == "__main__":
    unittest.main()
