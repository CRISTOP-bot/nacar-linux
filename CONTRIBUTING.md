# Contributing

Contributions should improve a real, testable part of the distribution. Small, reviewable pull requests are preferred; do not submit generated ISOs, caches, secrets, or large build trees.

## Before a pull request

1. Explain the problem and the design choice; link an architecture decision when one is needed.
2. Preserve existing behavior unless a documented technical reason justifies a change.
3. For third-party material, establish provenance, version, copyright, and license before inclusion; update `THIRD_PARTY.md` and keep all required notices.
4. Run `bash -n build.sh auto/config` and `python3 -m unittest discover -s tests -v`.
5. For build, package, init, or boot changes, report the exact Debian suite, tool versions, commands, and test results. Do not describe an untested configuration as working.
6. Keep secrets and private signing material out of Git. Use test-only credentials and explain how to reproduce without publishing them.

## Pull request expectations

A PR should state its scope, user-visible effect, license/provenance impact, tests run, known limitations, and follow-up work. Changes to package selection should include the reason each package is needed. Changes to startup should explain OpenRC runlevel/service behavior and verify that systemd is not an accidental requirement.

By submitting a contribution, you agree that it is offered under the repository's stated license for original project code, unless a separate written agreement says otherwise. Third-party code keeps its original terms.
