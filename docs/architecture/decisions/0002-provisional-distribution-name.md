# Decision 0002: provisional distribution name

- Date: 2026-10-05
- Status: provisional; use for the repository and development artifacts, not as a claim of trademark clearance

## Decision

Use **Nácar GNU/Linux** as the working distribution name and `nacar-linux` as its ASCII GitHub repository and artifact slug. The name evokes a lightweight, layered system; no logo, custom artwork, or final visual identity is selected.

A quick public web search and GitHub's public repository search for this exact name returned no results at the time of the check. This is not a complete trademark, company-name, domain, or legal search and does not establish that the name is available. Recheck before a public launch, and choose another name if a conflict is found.

## Attribution and scope

Nácar is an independent project based on Debian; the name does not imply that it is an official Debian project or that Debian endorses it. Debian and OpenRC retain their own names, marks, copyrights, and licenses. The working name is kept separate from the underlying build configuration so forks can replace it without editing the Debian/OpenRC engineering core.

## Consequences

- Use the display name `Nácar GNU/Linux` in project documentation and `nacar-linux` in repository and artifact filenames.
- Keep artwork, logo, colors, and boot theme out until their origin and licenses are reviewed.
- Keep the ISO release blocked until the documented boot, credential, licensing, and release gates pass.
