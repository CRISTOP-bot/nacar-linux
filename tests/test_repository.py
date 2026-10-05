# SPDX-License-Identifier: GPL-3.0-or-later
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class RepositoryPolicyTests(unittest.TestCase):
    def test_required_project_documents_exist(self):
        for name in (
            "README.md", "ROADMAP.md", "VERSION", "LICENSE", "COPYRIGHT",
            "THIRD_PARTY.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md",
            "SECURITY.md", "FORKING.md", "CHANGELOG.md", "docs/build-system.md",
            "docs/architecture/package-rationale.md",
            "docs/architecture/decisions/0002-provisional-distribution-name.md",
        ):
            with self.subTest(name=name):
                self.assertTrue((ROOT / name).is_file())

    def test_bootstrap_explicitly_selects_debian_and_openrc(self):
        config = (ROOT / "auto/config").read_text()
        packages = (ROOT / "config/package-lists/base.list.chroot").read_text().splitlines()
        package_names = {line.strip() for line in packages if line.strip() and not line.lstrip().startswith("#")}
        self.assertIn("--distribution trixie", config)
        self.assertIn("--binary-images iso-hybrid", config)
        self.assertIn("init=/usr/sbin/openrc-init", config)
        self.assertIn("openrc", package_names)
        self.assertIn("live-boot", package_names)
        self.assertNotIn("systemd-sysv", package_names)

    def test_provisional_name_and_artifact_slug_are_consistent(self):
        name_decision = (ROOT / "docs/architecture/decisions/0002-provisional-distribution-name.md").read_text()
        readme = (ROOT / "README.md").read_text()
        build = (ROOT / "build.sh").read_text()
        release = (ROOT / ".github/workflows/release-iso.yml").read_text()
        self.assertIn("Nácar GNU/Linux", name_decision)
        self.assertIn("nacar-linux", name_decision)
        self.assertIn("Nácar GNU/Linux", readme)
        self.assertIn('BASENAME="nacar-linux_', build)
        self.assertIn("dist/nacar-linux_*.iso", release)
        self.assertNotIn("openrc-debian_", build + release)

    def test_every_explicit_base_package_has_a_rationale(self):
        package_lines = (ROOT / "config/package-lists/base.list.chroot").read_text().splitlines()
        packages = [line.strip() for line in package_lines if line.strip() and not line.lstrip().startswith("#")]
        rationale = (ROOT / "docs/architecture/package-rationale.md").read_text()
        for package in packages:
            with self.subTest(package=package):
                self.assertIn(f"| `{package}` |", rationale)

    def test_no_placeholder_or_remote_shell_bootstrap(self):
        for rel in ("build.sh", "auto/config"):
            text = (ROOT / rel).read_text()
            self.assertNotRegex(text, re.compile(r"\bTODO\b|curl\s+[^|]+\|\s*(ba)?sh", re.IGNORECASE))

    def test_generated_outputs_are_ignored(self):
        ignore = (ROOT / ".gitignore").read_text().splitlines()
        self.assertIn("/dist/", ignore)
        self.assertIn("/build/", ignore)
        self.assertIn("*.iso", ignore)
        self.assertIn("*.build-info.txt", ignore)

    def test_build_protects_existing_artifacts(self):
        script = (ROOT / "build.sh").read_text()
        self.assertIn("Refusing to overwrite existing output", script)
        self.assertIn("mktemp -d", script)

    def test_build_metadata_records_provenance_without_claiming_reproducibility(self):
        script = (ROOT / "build.sh").read_text()
        for field in ("project_name=Nácar GNU/Linux", "source_revision", "builder_distribution", "live_build_version", "reproducibility_status=not-established"):
            with self.subTest(field=field):
                self.assertIn(field, script)
        self.assertIn(".build-info.txt", (ROOT / ".github/workflows/release-iso.yml").read_text())
        self.assertIn("*.build-info.txt", (ROOT / ".gitignore").read_text())

    def test_release_workflow_is_blocked_until_review(self):
        self.assertEqual((ROOT / "RELEASE_STATUS").read_text().strip(), "blocked")
        workflow = (ROOT / ".github/workflows/release-iso.yml").read_text()
        self.assertIn("release-ready", workflow)
        self.assertIn("VERSION", workflow)
        self.assertIn("tags:", workflow)
        self.assertIn("gh release create", workflow)
        self.assertNotIn("types: [published]", workflow)

    def test_third_party_policy_does_not_claim_all_packages_are_project_code(self):
        text = (ROOT / "THIRD_PARTY.md").read_text()
        self.assertIn("per-package copyright", text.lower())
        self.assertIn("No third-party source code", text)
        self.assertIn("Exact versions", text)

    def test_basic_secret_patterns_are_absent(self):
        patterns = (
            re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
            re.compile(r"\b(?:ghp|github_pat|glpat|gho)_[A-Za-z0-9_]{20,}\b"),
            re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
        )
        excluded = {".git", "__pycache__"}
        for path in ROOT.rglob("*"):
            if not path.is_file() or any(part in excluded for part in path.parts):
                continue
            try:
                content = path.read_text(errors="ignore")
            except OSError:
                continue
            for pattern in patterns:
                with self.subTest(path=str(path.relative_to(ROOT)), pattern=pattern.pattern):
                    self.assertIsNone(pattern.search(content), "Possible secret found; remove it and rotate the credential")


if __name__ == "__main__":
    unittest.main()
