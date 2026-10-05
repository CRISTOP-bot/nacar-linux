# Decision 0002: provisional distribution name

- Date: 2026-10-05
- Status: provisional; use for the repository and development artifacts, not as a claim of trademark clearance

## Decision

Use **Nácar GNU/Linux** as the working distribution name, `nacar-linux` as its ASCII GitHub repository slug, and `nacar.iso` as the ISO filename. User-facing operating-system and ISO metadata identify Nácar, while Debian technical provenance and required notices remain intact. The name evokes a lightweight, layered system; no logo, custom artwork, or final visual identity is selected.

A quick public web search and GitHub's public repository search for this exact name returned no results at the time of the check. This is not a complete trademark, company-name, domain, or legal search and does not establish that the name is available. Recheck before a public launch, and choose another name if a conflict is found.

## Attribution and scope

Nácar is an independent project based on Debian; the name does not imply that it is an official Debian project or that Debian endorses it. Debian and OpenRC retain their own names, marks, copyrights, and licenses. The working name is kept separate from the underlying build configuration so forks can replace it without editing the Debian/OpenRC engineering core.

## Consequences

- Use `Nácar GNU/Linux` for the display identity, `nacar-linux` for the GitHub repository slug, and `nacar.iso` plus `nacar.*` for generated ISO artifacts and sidecars.
- Keep artwork, logo, colors, and boot theme out until their origin and licenses are reviewed.
- Keep the ISO release blocked until the documented boot, credential, licensing, and release gates pass.
