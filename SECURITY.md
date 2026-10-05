# Security policy

This is an early development project and has no supported production release. Do not install it on systems containing important data.

## Reporting a vulnerability

Do not put exploit details, credentials, private keys, or personal information in a public issue. Use GitHub's private vulnerability reporting if enabled for the repository; otherwise contact the maintainers privately using the contact method published in the repository. A security report should include affected revision, impact, reproduction steps, and any proposed mitigation. Do not include real user data.

## Development security requirements

- Never commit passwords, access tokens, API keys, signing keys, private certificates, or real user data.
- Use Debian's signed repository metadata; do not pipe downloaded scripts into a shell.
- Do not run unreviewed build hooks as root. Review all hook and installer changes before building.
- Keep the live system's credentials and remote-access policy explicit; the initial Live configuration is not release-safe until its default credentials are replaced and tested.
- Review package dependencies for systemd-only assumptions and privilege requirements.
- Enable GitHub secret scanning and push protection, branch protection, and private vulnerability reporting in repository settings when available. Workflow checks are not a replacement for those controls.

Security updates and supported release branches will be defined before a stable release.
