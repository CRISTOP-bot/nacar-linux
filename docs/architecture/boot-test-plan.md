# Boot test plan (release gate)

No test result is recorded until these steps run against a built image. The manual build verifier also checks that the installed live-config user-setup component sorts before its hooks component; this structural check does not prove runtime execution or user creation.

## Test matrix

| Firmware | Machine | Required evidence |
| --- | --- | --- |
| BIOS | QEMU `pc`/SeaBIOS, amd64 | Image starts, kernel/initramfs load, interactive console and shell are usable |
| UEFI | QEMU `q35` + OVMF, amd64 | EFI boot succeeds without a pre-existing host disk |

## Assertions

1. Boot with no writable host disk attached; use a disposable disk for installer tests only.
2. Confirm kernel, initramfs, root filesystem, and interactive console.
3. Confirm PID 1 is `/usr/sbin/openrc-init`, `rc-status` reports a sensible runlevel, and `rc-service` controls a test service.
4. Confirm intended OpenRC service scripts are enabled and no systemd init/service manager is required or running.
5. Verify DHCP and DNS in an isolated QEMU user network; separately record hardware firmware limitations.
6. Check shutdown/reboot and inspect console/kernel logs for failed units, service loops, and permission errors.
7. Verify the per-boot Live password is visible only on the local console, allows the intended login/admin path, and does not appear in saved logs; repeat with and without persistence.
8. Record QEMU/OVMF versions, exact command lines, image SHA-256, package inventory, and logs; redact the credential from any retained console capture.

## Safety

Never attach a developer's real block device to automated installer tests. Use a freshly created disposable image, verify the guest sees only that test disk, and require an explicit confirmation path before any destructive installer operation.
