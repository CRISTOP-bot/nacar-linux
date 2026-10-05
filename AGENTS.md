# Repository guidance for coding agents

These instructions apply to the whole Nácar GNU/Linux repository. They complement `CONTRIBUTING.md`; they do not replace the project's architecture decisions, security policy, or user instructions.

## Mission and scope

- Work only in this repository: Nácar GNU/Linux, an experimental amd64 live-image project based technically on Debian Trixie and intended to use OpenRC.
- Do not inspect, copy from, or mix in unrelated OS projects, even when their names look similar.
- Before a non-trivial change, read `README.md`, `ROADMAP.md`, `docs/README.md`, and the relevant architecture, build, security, and verification documents.
- Check the repository status and existing implementation before editing. Preserve unrelated user changes.

## Engineering invariants

- Treat the project as experimental. Distinguish **implemented**, **experimental**, and **planned** work. Never claim that a build, boot, installer, or service works without evidence for that exact claim.
- The target is Debian Trixie amd64. OpenRC is intended as PID 1 through `/usr/sbin/openrc-init`; this remains unverified until a booted image demonstrates it.
- Keep Debian provenance truthful. Do not remove required copyright, license, package-origin, repository, or compatibility metadata to make the project appear independent. Branding changes apply to user-visible Nácar surfaces only.
- Keep the base minimal. Every explicitly selected package needs a rationale in `docs/architecture/package-rationale.md`. Do not add systemd as a workaround for a dependency conflict; inspect and document the package graph while preserving the OpenRC goal.
- Prefer real, testable implementations. Do not add fake commands, success-only stubs, unverified scaffolding, or claims unsupported by tests.
- Do not add destructive disk behavior. Storage/install experiments belong on disposable QEMU disks and must include dry-run and explicit confirmation safeguards.

## Public-repository and release safety

- Never commit credentials, private keys, personal data, generated ISO files, build caches, or unpublished signing material.
- The manual public GitHub Actions workflow must not upload or retain `nacar.iso` or its sidecars. Its runner discards generated output at job end. Do not reintroduce artifact upload without explicit user authorization and a reviewed access policy.
- Do not publish an ISO, create a release or tag, change repository visibility, alter secrets, or push changes unless the user explicitly asks for that external action.
- Keep `RELEASE_STATUS` set to `blocked` until every release gate in `ROADMAP.md` and `docs/architecture/boot-test-plan.md` has verifiable evidence. A successful build or static CI run alone is not release approval.
- Do not run destructive Git commands (`reset --hard`, force-push, history rewrite) or overwrite existing build outputs.

## Change workflow

1. State the scope and inspect the files and tests that own the behavior.
2. Make a small, reviewable change; update documentation when behavior, risk, or status changes.
3. Run the relevant checks below. Report exact failures and limitations; do not suppress them to obtain a green result.
4. Inspect the diff and repository status. Keep generated outputs out of version control.
5. Create a checkpoint commit for substantial multi-step work when appropriate. Push or publish only with explicit user authorization.

## Standard checks

Run from the repository root:

```sh
bash -n build.sh
sh -n auto/config
sh -n config/includes.chroot/usr/lib/live/config-hooks/9999-nacar-live-credentials
sh -n tests/verify_live_image.sh
sh -n scripts/build_in_container.sh
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/*.py tests/*.py
```

`./build.sh --check` validates local prerequisites. `./build.sh` attempts a real local build and writes `dist/nacar.iso`, `dist/nacar.packages.tsv`, `dist/nacar.build-info.txt`, and `dist/nacar.sha256` only when successful. It may require root privileges and Debian Live build dependencies; do not describe a failed build as success.

For a built image, run:

```sh
tests/verify_live_image.sh dist/nacar.iso dist/nacar.packages.tsv
```

This inspects ISO metadata, boot-menu branding, package contents, hook files, and static live-config order. **It is not a boot test.** Follow `docs/architecture/boot-test-plan.md` for QEMU BIOS/UEFI and runtime checks. Never use a host disk for installation tests.

## Evidence and reporting

- Record the tested commit, command, environment/tool versions where available, result, and remaining blockers.
- Separate source/unit tests, a completed ISO build, static image inspection, QEMU runtime tests, and release approval; they prove different things.
- If a workflow or build fails, report its actual failing step and concise logs. Do not dispatch duplicate long builds while one is still running.
- Consult `docs/README.md` for the documentation map and `docs/verification-model.md` for evidence levels and release claims.
