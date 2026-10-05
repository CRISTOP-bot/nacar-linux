# Live image credentials: release blocker

Debian Live documents a default live account and password. A public image must not ship with an undocumented or shared default password.

## Experimental implementation

The repository now contains `config/includes.chroot/usr/lib/live/config-hooks/9999-nacar-live-credentials`, activated by `live-config.hooks=filesystem` in the experimental boot configuration. At boot, the hook:

- requires root, the existing `live` account, `chpasswd`, and a writable local `/dev/console`;
- saves the prior shadow password field in memory, generates 10 random bytes, and encodes them as a 16-character Base32 password;
- sends the new password to `chpasswd` through standard input, never as an argument or saved file;
- writes the password only to the local kernel console; if setting or displaying it fails, attempts to restore the prior password hash;
- unsets the password and saved hash from its shell state before exiting.

This is **experimental code, not a validated credential policy**. Its exact run order relative to live-user setup and getty, its console visibility under `openrc-init`, and its behavior with persistence have not been tested in a built image. Do not publish an ISO based on this implementation yet. The generated console output is secret-bearing: never put raw serial-console logs in public CI artifacts.

## Required validation before M1 completion

1. Verify the hook is included at `/usr/lib/live/config-hooks/9999-nacar-live-credentials` and `live-config.hooks=filesystem` activates it in the built image.
2. Confirm `live-config` creates the `live` account before the hook and the hook runs before the login/getty path that needs the password.
3. Test successful password rotation and both failure/rollback paths in QEMU; test BIOS and UEFI with `openrc-init` as PID 1.
4. Verify that no password appears in argv, build output, `live-config` logs, CI output, or uploaded artifacts; only the local console may show it.
5. Reboot with and without persistence and confirm each session has a usable credential without a shared default.

Reference: [Debian Trixie `live-config(7)`](https://manpages.debian.org/trixie/live-config-doc/live-config.7.en.html). The manual documents filesystem hooks in `/usr/lib/live/config-hooks/` and the `live-config.hooks=filesystem` option; that does not prove this project's hook ordering or runtime behavior.
