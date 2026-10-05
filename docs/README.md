# Documentation index

Use this page to find the current source of truth for design, implementation, verification, and release readiness. When a status statement becomes stale, update the owning document rather than relying on an old chat or workflow summary.

## Start here

| Topic | Document | What it answers |
| --- | --- | --- |
| Project overview | [`../README.md`](../README.md) | What Nácar is, its technical base, current scope, and how to run checks |
| Agent-specific workflow | [`../AGENTS.md`](../AGENTS.md) | Repository boundaries, engineering invariants, safety rules, and standard commands |
| Work priorities | [`../ROADMAP.md`](../ROADMAP.md) | Milestones, proof required, and open blockers |
| Release gate | [`../RELEASE_STATUS`](../RELEASE_STATUS) | Whether an ISO release is authorized; `blocked` is not the same as a successful build |
| Contributing | [`../CONTRIBUTING.md`](../CONTRIBUTING.md) | Expectations for a pull request and contribution evidence |

## Engineering and operations

| Area | Document | Scope |
| --- | --- | --- |
| Development workflow | [`development-workflow.md`](development-workflow.md) | Change sequence, tests, build outputs, CI limits, and failure reporting |
| Verification model | [`verification-model.md`](verification-model.md) | What static tests, image inspection, QEMU tests, and release approval prove |
| Build system | [`build-system.md`](build-system.md) | `live-build`, branding, generated outputs, provenance, and build limitations |
| Boot and runtime tests | [`architecture/boot-test-plan.md`](architecture/boot-test-plan.md) | BIOS/UEFI QEMU matrix and runtime checks required before release |
| Repository boundaries | [`architecture/repository-layout.md`](architecture/repository-layout.md) | Responsibilities and separation of repository areas |
| Package selection | [`architecture/package-rationale.md`](architecture/package-rationale.md) | Reason and verification status for each explicitly selected base package |
| OpenRC/live-image design | [`architecture/decisions/0001-bootstrap-and-live-builder.md`](architecture/decisions/0001-bootstrap-and-live-builder.md) | Initial Debian Live and OpenRC design choices |
| Provisional name | [`architecture/decisions/0002-provisional-distribution-name.md`](architecture/decisions/0002-provisional-distribution-name.md) | Working name, repository slug, and naming limits |
| Live credentials | [`security/live-credentials.md`](security/live-credentials.md) | Per-boot credential hook risks, safeguards, and unverified behavior |
| Project license | [`licensing/decision-0001-project-license.md`](licensing/decision-0001-project-license.md) | License for original code and treatment of upstream works |
| Third-party inventory | [`../THIRD_PARTY.md`](../THIRD_PARTY.md) | Upstream origins, notices, modifications, and package-level obligations |

## Status vocabulary

- **Implemented:** a real behavior exists and has a corresponding executable test or runtime demonstration; the claim must name the evidence.
- **Experimental:** code or configuration exists but has not passed the required end-to-end or boot tests.
- **Planned:** a documented intention without a completed implementation.
- **Blocked:** a release or milestone gate is not satisfied. Static CI passing does not clear a build, boot, licensing, or security blocker.

For the latest result, inspect the current commit's GitHub Actions run and the exact test output. Do not infer that an ISO exists just because a workflow was dispatched.
