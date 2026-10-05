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
for tool in xorriso unsquashfs awk python3; do
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
grep -Fqx 'ID=nacar' "$ROOTFS/etc/os-release"
grep -Fqx 'ID_LIKE=debian' "$ROOTFS/etc/os-release"
grep -Fq 'Nácar GNU/Linux' "$ROOTFS/etc/os-release"
grep -Fq 'Nácar GNU/Linux' "$ROOTFS/etc/issue"
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd -P)"
python3 "$SCRIPT_DIR/../scripts/check_iso_metadata.py" "$ISO"
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
xorriso -osirrox on -indev "$ISO" -extract /isolinux "$TMPDIR_VERIFY/isolinux" >/dev/null 2>&1
xorriso -osirrox on -indev "$ISO" -extract /boot/grub "$TMPDIR_VERIFY/grub" >/dev/null 2>&1
python3 "$SCRIPT_DIR/../scripts/check_boot_branding.py" "$TMPDIR_VERIFY/isolinux" "$TMPDIR_VERIFY/grub"

# live-config components run in numeric filename order; the user's account
# must exist before the custom filesystem hook is executed by the hooks component.
COMPONENT_DIR="$ROOTFS/usr/lib/live/config"
USER_SETUP="$(find "$COMPONENT_DIR" -maxdepth 1 -type f -name '*-user-setup' -print -quit)"
HOOK_RUNNER="$(find "$COMPONENT_DIR" -maxdepth 1 -type f -name '*-hooks' -print -quit)"
[ -n "$USER_SETUP" ] || { printf 'Cannot locate live-config user-setup component.\n' >&2; exit 1; }
[ -n "$HOOK_RUNNER" ] || { printf 'Cannot locate live-config hooks component.\n' >&2; exit 1; }
component_order() {
    component_name=${1##*/}
    case "$component_name" in
        [0-9][0-9][0-9][0-9]-*) printf '%s\n' "${component_name%%-*}" ;;
        *) return 1 ;;
    esac
}
USER_ORDER="$(component_order "$USER_SETUP")" || { printf 'Unexpected user-setup component name: %s\n' "$USER_SETUP" >&2; exit 1; }
HOOK_ORDER="$(component_order "$HOOK_RUNNER")" || { printf 'Unexpected hooks component name: %s\n' "$HOOK_RUNNER" >&2; exit 1; }
if [ "$USER_ORDER" -ge "$HOOK_ORDER" ]; then
    printf 'Unsafe live-config order: user setup %s must precede hooks %s.\n' "$USER_SETUP" "$HOOK_RUNNER" >&2
    exit 1
fi
printf 'live-config order verified: %s precedes %s.\n' "${USER_SETUP##*/}" "${HOOK_RUNNER##*/}"
printf '%s\n' 'Nacar ISO branding, package inventory, OpenRC init, credential tools, and hook files verified.'
printf '%s\n' 'These checks do not prove boot, PID 1, networking, or runtime hook execution.'
