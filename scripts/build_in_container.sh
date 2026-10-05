#!/bin/bash
# SPDX-License-Identifier: GPL-3.0-or-later
# Run only inside the isolated Debian Trixie build container with mount privileges.
set -Eeuo pipefail

if (( EUID != 0 )); then
    printf '%s\n' 'Image build container must run as root.' >&2
    exit 1
fi

apt-get update
apt-get install --yes --no-install-recommends \
    bash ca-certificates dosfstools grub-efi-amd64-bin grub-pc-bin \
    live-build mtools python3 rsync squashfs-tools syslinux-common \
    syslinux-utils util-linux xorriso

./build.sh
(cd dist && sha256sum --check nacar.sha256)
bash tests/verify_live_image.sh dist/nacar.iso dist/nacar.packages.tsv
