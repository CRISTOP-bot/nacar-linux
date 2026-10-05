#!/bin/sh
# SPDX-License-Identifier: GPL-3.0-or-later
# Verify packaged components in a built Debian Live ISO; this is not a boot test.
set -eu

if [ "$#" -ne 2 ]; then
    printf 'Usage: %s IMAGE.iso PACKAGE-INVENTORY.tsv\n' "$0" >&2
    exit 2
fi
ISO=$1
PACKAGES=$2
[ -f "$ISO" ] || { printf 'ISO not found: %s\n' "$ISO" >&2; exit 1; }
[ -f "$PACKAGES" ] || { printf 'Package inventory not found: %s\n' "$PACKAGES" >&2; exit 1; }
for tool in xorriso unsquashfs awk; do
    command -v "$tool" >/dev/null 2>&1 || { printf 'Missing verifier tool: %s\n' "$tool" >&2; exit 1; }
done

package_present() {
    awk -F '\t' -v package="$1" '$1 == package || $1 ~ ("^" package ":[^:]+$") { found=1 } END { exit !found }' "$PACKAGES"
}
for package in linux-image-amd64 live-boot live-config live-config-sysvinit openrc passwd coreutils; do
    package_present "$package" || { printf 'Required package is absent from inventory: %s\n' "$package" >&2; exit 1; }
done

TMPDIR_VERIFY="$(mktemp -d "${TMPDIR:-/tmp}/nacar-live-verify.XXXXXXXX")"
cleanup() { rm -rf -- "$TMPDIR_VERIFY"; }
trap cleanup EXIT HUP INT TERM

xorriso -osirrox on -indev "$ISO" -extract /live/filesystem.squashfs "$TMPDIR_VERIFY/filesystem.squashfs" >/dev/null 2>&1
unsquashfs -no-progress -d "$TMPDIR_VERIFY/rootfs" "$TMPDIR_VERIFY/filesystem.squashfs" >/dev/null
ROOTFS="$TMPDIR_VERIFY/rootfs"
for file in \
    usr/sbin/openrc-init \
    usr/sbin/chpasswd \
    usr/bin/base32 \
    usr/bin/dd \
    usr/bin/tr \
    usr/bin/getent \
    usr/lib/live/config-hooks/9999-nacar-live-credentials; do
    [ -x "$ROOTFS/$file" ] || { printf 'Missing or non-executable image file: /%s\n' "$file" >&2; exit 1; }
done
printf '%s\n' 'ISO package inventory, OpenRC init, credential tools, and executable hook verified.'
printf '%s\n' 'This check does not prove boot, PID 1, network, or hook order.'
