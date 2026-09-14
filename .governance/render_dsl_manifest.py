#!/usr/bin/env python3
"""Project adopted package ownership; never update the lock or grant authority."""

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import tempfile

OUTPUT = ".governance/dsl-manifest.json"
SOURCE = ".governance/manifest.schema.json"
DSL_REVISION = "b7d0595c95e5abbb48ebfdbdae0bc6d43c6f82f4"


def local_path(root, name):
    parts = PurePosixPath(name).parts
    if not parts or name.startswith("/") or ".." in parts or "\\" in name:
        raise ValueError(f"unsafe package path: {name}")
    result = root
    for part in parts:
        result = result / part
        if result.is_symlink():
            raise ValueError(f"symlink package path: {name}")
    return result


def project(root):
    lock = json.loads(local_path(root, ".governance/manifest.lock.json").read_bytes())
    pin = lock["standard"]
    if (lock["schema"] != "new-project.lock/v1"
            or pin["id"] != "wellmanifest/new-project"
            or pin["sourceRepository"] != "wellmanifest/new-project"
            or pin["publicationStatus"] != "published"
            or not re.fullmatch(r"[0-9a-f]{40}", pin["sourceRevision"])
            or not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", pin["version"])):
        raise ValueError("a published new-project immutable pin is required")
    managed = lock["managedFiles"]
    if not isinstance(managed, dict) or SOURCE not in managed or OUTPUT in managed:
        raise ValueError("invalid managed file map or projection self-ownership")
    artifacts = []
    for name, digest in sorted(managed.items()):
        content = local_path(root, name).read_bytes()
        if hashlib.sha256(content).hexdigest() != digest:
            raise ValueError(f"managed digest mismatch: {name}")
        role = "profile"
        if name == SOURCE:
            role = "normative-source"
        elif name.endswith("schema.json"):
            role = "schema"
        elif name.endswith((".py", ".sh", ".bat")):
            role = "parser-contract"
        elif name.endswith(".md"):
            role = "documentation"
        artifacts.append({"path": name, "role": role, "digest": "sha256:" + digest})
    return {
        "$schema": f"https://raw.githubusercontent.com/wellmanifest/dsl/{DSL_REVISION}/schemas/dsl-manifest.schema.json",
        "schema": "wellmanifest.dsl/manifest/v1",
        "id": "wellmanifest.deployment.adopted-governance",
        "name": "Adopted new-project governance package",
        "version": pin["version"], "status": "experimental",
        "purpose": "Digest-bound ownership projection of the adopted package; semantics remain at wellmanifest/new-project and trusted approval remains external",
        "domain": "software-governance",
        "owners": [{"kind": "repository", "id": "github:wellmanifest/new-project",
                    "responsibilities": ["semantics", "validation", "compatibility", "security"]}],
        "source": {"repository": "https://github.com/wellmanifest/new-project",
                   "path": SOURCE, "revision": pin["sourceRevision"],
                   "declaredVersion": pin["version"], "canonical": "json-ast",
                   "mediaType": "application/schema+json", "selectors": []},
        "ownedPaths": [OUTPUT, *sorted(managed)], "artifacts": artifacts,
        "namespaces": [{"prefix": "new-project", "uri": "https://github.com/wellmanifest/new-project/"}],
        "projections": [],
        "lifecycle": {"compatibility": "semver", "stability": "experimental",
                      "breaking": "major", "additive": "minor", "fix": "patch"},
        "semantics": {"effectModel": "declarative-policy", "unknownPolicy": "reject", "authoritySchema": None},
        "llm": {"mode": "none", "requestSchemas": [], "responseSchemas": [],
                "naturalLanguage": "forbidden", "sourceSchema": None, "modelAuthority": "none", "strict": True},
        "documentation": {"vocabularyKind": "documents", "commandRoot": "docs",
                          "errorRoot": "docs/ERROR", "criticalRoot": "docs/CRITICAL",
                          "commands": [], "errorCodes": [], "criticalCodes": []},
        "findingPolicy": {"schema": "wellmanifest.dsl/findings/v1",
                          "requiredProducers": ["wellmanifest.new-project.governance-check"],
                          "securityProducers": ["wellmanifest.new-project.governance-check"],
                          "blockingSeverities": ["error", "critical"],
                          "requireEvaluable": True, "blockUnresolvedSecurity": True},
        "publicationPolicy": {"declaredTier": "review", "deterministic": True,
                              "independentReview": True, "externalAuthority": False, "runtimeIsolation": False},
        "conformance": {"levels": ["manifest"],
                        "commands": ["python3 .governance/render_dsl_manifest.py --check", "./project/governance-check.sh"],
                        "validExamples": [], "invalidExamples": []},
        "mappings": [{"standard": "wellmanifest.new-project", "version": pin["version"],
                      "relation": "implements", "uri": "https://github.com/wellmanifest/new-project/tree/" + pin["sourceRevision"]}],
        "standardsLock": {"schema": "wellmanifest.standards-lock/v1", "entries": [
            {"standard": "wellmanifest.new-project", "version": pin["version"],
             "repository": "https://github.com/wellmanifest/new-project", "revision": pin["sourceRevision"],
             "contracts": [{"ref": "https://github.com/wellmanifest/new-project/blob/" + pin["sourceRevision"] + "/governance/manifest.schema.json",
                            "digest": "sha256:" + managed[SOURCE]}]}]},
    }


def render(root, check=False):
    content = (json.dumps(project(root), indent=2, ensure_ascii=False) + "\n").encode()
    target = local_path(root, OUTPUT)
    if check:
        if not target.is_file() or target.read_bytes() != content:
            raise ValueError("adopted DSL projection is stale; run python3 .governance/render_dsl_manifest.py")
        return
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=target.parent, prefix=".dsl-projection-", delete=False) as stream:
            temporary = Path(stream.name)
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, target)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        render(args.root.resolve(), args.check)
    except (ValueError, OSError, KeyError, TypeError) as error:
        parser.exit(1, f"adopted DSL projection failed: {error}\n")
    print("adopted DSL projection: PASS" if args.check else "adopted DSL projection: rendered")


if __name__ == "__main__":
    main()
