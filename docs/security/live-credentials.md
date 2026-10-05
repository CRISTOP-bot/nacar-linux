# Live image credentials: release blocker

Debian Live documents a default live account and password. The current bootstrap sets a distinct live username but does **not yet implement a reviewed replacement credential mechanism**. A public image must not ship with an undocumented or shared default password.

Before M1 is complete, implement and test a per-boot random credential with a safe local presentation path; do not store it in Git, the ISO, or public build logs. The Debian Trixie `live-config(7)` documentation exposes filesystem hooks in `/usr/lib/live/config-hooks/`, activated through `live-config.hooks=filesystem`; it notes that live-config also requires an init-system backend. A hook is therefore a possible integration point, not yet a verified solution. It must confirm the `live` account exists, generate a high-entropy password at runtime, feed it to the account tool over stdin (not argv or logs), and display it only on the local console. If it cannot safely show the credential or the target account is missing, it must fail closed and must not leave the account with an unknown replacement password.

Before enabling such a hook in `auto/config`, verify its order relative to the live-user-setup and getty components in the built image, ensure passwords never enter CI logs, and test the exact behavior under `openrc-init` with and without persistence. Do not copy Debian's example hook without reviewing its exact license/copyright and documenting the source. Do not assume a blank or locked password is safe or usable without testing.

Reference: [Debian Trixie `live-config(7)`](https://manpages.debian.org/trixie/live-config-doc/live-config.7.en.html).
