# Development workflow

This guide describes how to make a small, reviewable change and gather evidence for it. For repository-specific safety rules, see [`../AGENTS.md`](../AGENTS.md); for test meanings, see [`verification-model.md`](verification-model.md).

## 1. Establish the current state

Before editing:

1. Read `README.md`, `ROADMAP.md`, `RELEASE_STATUS`, and the relevant decision or subsystem document.
2. Inspect the target files and tests; do not infer behavior from names or plans.
3. Check the current Git status and preserve any unrelated changes.
4. Confirm the current commit and latest validation/build workflow results. A previous successful run does not validate later commits.

Keep scope inside the Nácar repository. Do not inspect or combine similarly named operating-system projects.

## 2. Make changes with evidence

- Prefer the smallest change that addresses a concrete problem.
- For every package change, add or update its entry in `docs/architecture/package-rationale.md`, including its role and verification status.
- For boot, init, credentials, or package-closure changes, explain the effect on OpenRC and Debian Live; add a regression test where practical.
- Update the owning documentation when an implementation, risk, decision, or status changes. Keep `ROADMAP.md` and `RELEASE_STATUS` truthful.
- Preserve copyright, license, and package-origin metadata. User-visible branding does not change the Debian technical base.
- Do not introduce stubs or claim an end-to-end feature from a unit test alone.

## 3. Run source checks

From the repository root:

```sh
bash -n build.sh
sh -n auto/config
sh -n config/includes.chroot/usr/lib/live/config-hooks/9999-nacar-live-credentials
sh -n tests/verify_live_image.sh
sh -n scripts/build_in_container.sh
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/*.py tests/*.py
```

The GitHub `Validate repository` workflow runs source-level checks for the commit. A green validation run does not mean that the image built or booted. Record the exact command and result for any test you run locally.

## 4. Build and inspect the image

`./build.sh --check` checks local prerequisites. `./build.sh` invokes `live-build` and, only after a successful build and checks, places the following files under ignored `dist/`:

- `nacar.iso`
- `nacar.packages.tsv`
- `nacar.build-info.txt`
- `nacar.sha256`

The script uses a fresh temporary build tree and refuses to overwrite existing outputs. A build may require `sudo` and the packages listed in `README.md` and `docs/build-system.md`. If dependency resolution fails, inspect the exact APT conflict and package closure; do not add a conflicting init system as a shortcut.

For an image that actually exists, run:

```sh
tests/verify_live_image.sh dist/nacar.iso dist/nacar.packages.tsv
```

This verifies selected image contents, metadata, visible branding, and static hook ordering. It does not boot the image or prove PID 1, networking, or credential-hook runtime behavior.

## 5. Understand public CI output

The manual `Build and inspect Nácar ISO` workflow runs in an isolated privileged Debian Trixie container and performs static image inspection. Because the repository is public, it deliberately does **not** upload or retain the ISO or sidecars. The GitHub-hosted runner discards the output at job end. Do not re-add an artifact upload or publish an ISO without explicit authorization and a reviewed distribution policy.

The workflow is not a substitute for the QEMU matrix in [`architecture/boot-test-plan.md`](architecture/boot-test-plan.md). Never report a build as successful before the workflow's build and verification steps complete successfully.

## 6. Review and report

Before presenting a change:

- Review the diff and ensure no generated image, cache, credential, or unrelated file is included.
- Run the applicable checks again after the final edit.
- State what changed, the exact tests and commit they cover, and what remains unverified.
- Create checkpoint commits for substantial work when useful, but do not push, tag, release, alter repository visibility, or publish build outputs without explicit user authorization.
