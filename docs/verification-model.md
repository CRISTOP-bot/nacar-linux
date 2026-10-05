# Verification model and evidence levels

Use this model when describing project maturity. Evidence at one level does not automatically satisfy a later level. The detailed QEMU test procedure is in [`architecture/boot-test-plan.md`](architecture/boot-test-plan.md); the authoritative release gate is the root [`RELEASE_STATUS`](../RELEASE_STATUS) file.

## Evidence ladder

| Level | Required evidence | What it supports | What it does not support |
| --- | --- | --- | --- |
| Source checks | Shell syntax checks, Python unit tests, policy checks, and CI results for the exact commit | The checked source parses and the covered test cases pass | Successful dependency resolution, an ISO, or runtime behavior |
| Image build | A completed `live-build` run that produces `nacar.iso` and sidecars without error | The build completed in the recorded environment | Bootability, correct PID 1, working networking, or reproducibility |
| Static image inspection | `tests/verify_live_image.sh` passes against that exact ISO and package inventory | Required files/packages and selected ISO, boot-menu, hook, and ordering properties are present | Hook execution, console behavior, BIOS/UEFI boot, or overall usability |
| Runtime boot tests | Recorded QEMU BIOS and UEFI boots with logs, checksums, and the assertions in the boot-test plan | Only the behaviors actually observed in those runs | Untested hardware, installations, persistence modes, or reproducibility |
| Release approval | Every applicable release gate reviewed; `RELEASE_STATUS` explicitly changed through the approved process | A release may be considered under the documented policy | Any claim beyond the tested release scope |

## Claims and status words

- **Implemented:** the behavior exists and has passing evidence appropriate to its claim. Cite the test or runtime result.
- **Experimental:** a real implementation or configuration exists, but the needed end-to-end evidence is missing.
- **Planned:** a design intention, not a working feature.
- **Blocked:** a required gate has not passed. A green source-validation workflow does not override a failed image build or missing boot tests.

Use precise statements such as “the package inventory contains OpenRC” rather than “OpenRC works as PID 1” unless the image has booted and the PID 1 assertion passed.

## Image-inspection boundary

The verifier can inspect the SquashFS, ISO metadata, boot-menu text, package inventory, credential-hook files, and numeric live-config component order. Numeric order is only static evidence: it does not prove that the hook is invoked, that the `live` user exists at runtime, that `/dev/console` is available, or that rollback works in the actual image.

The manual public GitHub Actions workflow does not retain or upload generated images. If a build output is needed for private review, arrange an explicitly approved private destination; do not make the experimental ISO public by attaching it to a public workflow run.

## Runtime and release evidence

Before any release-readiness claim, follow the full matrix in `architecture/boot-test-plan.md`, including BIOS and UEFI, OpenRC as PID 1, `rc-status`, local console and credential-hook behavior, network/DNS, storage visibility, persistence cases, and clean shutdown/reboot. Use disposable QEMU disks only; never test installation against a host or personal disk.

Reproducibility is a separate claim. It requires pinned or otherwise immutable inputs and at least two isolated builds whose normalized outputs are compared and explained. A checksum proves the identity of one file, not that another build is reproducible.

Always check the exact source commit and current workflow run. Update `ROADMAP.md` and supporting documents when evidence changes; do not infer current status from a past conversation or a previous commit.
