# Live image credentials: release blocker

Debian Live documents a default live account and password. The current bootstrap sets a distinct live username but does **not yet implement a reviewed replacement credential mechanism**. A public image must not ship with an undocumented or shared default password.

Before M1 is complete, choose and test one of these designs: no interactive login unless a user explicitly configures it; or a per-boot/per-build random credential with a safe local presentation path and no secret stored in Git or in a public build log. Confirm the implementation works with the OpenRC init path and the exact `live-config` sequence. Do not assume a blank or locked password is safe or usable without testing.
