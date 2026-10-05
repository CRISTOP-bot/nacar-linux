#!/usr/bin/env bash
# SPDX-License-Identifier: GPL-3.0-or-later
set -Eeuo pipefail
IFS=$'\n\t'

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
VERSION="$(<"$ROOT/VERSION")"
if [[ ! "$VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+(-[A-Za-z0-9.-]+)?$ ]]; then
    printf 'Invalid VERSION value: %s\n' "$VERSION" >&2
    exit 2
fi

usage() {
    cat <<'USAGE'
Usage: ./build.sh [--check|--help]

Build an amd64 Debian Trixie Live ISO with OpenRC requested as PID 1.
The build uses new temporary directories and will not overwrite files in dist/.

  --check   Check host build prerequisites only; do not build.
  --help    Show this help.

Run as a normal user; the script requests sudo only for live-build's root-only
build stage. Do not run this on a production system: review build hooks first.
USAGE
}

need() {
    if ! command -v "$1" >/dev/null 2>&1; then
        printf 'Missing required host command: %s\n' "$1" >&2
        return 1
    fi
}

check_prerequisites() {
    local failed=0
    for tool in lb sha256sum dpkg-query find mktemp cp sort chroot head mkdir basename mv rm date; do
        need "$tool" || failed=1
    done
    if (( EUID != 0 )); then
        need sudo || failed=1
    fi
    if (( failed )); then
        printf '%s\n' 'Install Debian live-build and its documented image-building dependencies, then retry.' >&2
        return 1
    fi
    printf 'live-build: %s\n' "$(lb --version 2>&1 | head -n 1)"
    printf 'Target: Debian Trixie amd64; project version: %s\n' "$VERSION"
}

case "${1:-}" in
    --help|-h) usage; exit 0 ;;
    --check) check_prerequisites; exit $? ;;
    "") ;;
    *) printf 'Unknown option: %s\n' "$1" >&2; usage >&2; exit 2 ;;
esac

check_prerequisites
OUT="$ROOT/dist"
BASENAME="openrc-debian_${VERSION}_amd64.iso"
PACKAGE_BASENAME="openrc-debian_${VERSION}_amd64.packages.tsv"
INFO_BASENAME="openrc-debian_${VERSION}_amd64.build-info.txt"
SUMS_BASENAME="openrc-debian_${VERSION}_amd64.sha256"
for name in "$BASENAME" "$PACKAGE_BASENAME" "$INFO_BASENAME" "$SUMS_BASENAME"; do
    if [[ -e "$OUT/$name" || -L "$OUT/$name" ]]; then
        printf 'Refusing to overwrite existing output: %s\n' "$OUT/$name" >&2
        exit 1
    fi
done

BUILD_STARTED_UTC="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
SOURCE_REVISION="${GITHUB_SHA:-unknown}"
SOURCE_REF="${GITHUB_REF_NAME:-local}"
mkdir -p -- "$ROOT/build"
WORKDIR=""
STAGING=""
cleanup() {
    local status=$?
    trap - EXIT
    # Remove only the two fresh paths created by mktemp in this invocation.
    for path in "$WORKDIR" "$STAGING"; do
        [[ -n "$path" && -d "$path" ]] || continue
        if (( EUID == 0 )); then
            rm -rf -- "$path" || printf 'Could not remove generated temporary directory: %s\n' "$path" >&2
        else
            sudo rm -rf -- "$path" || printf 'Could not remove generated temporary directory: %s\n' "$path" >&2
        fi
    done
    exit "$status"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM

WORKDIR="$(mktemp -d "${TMPDIR:-/tmp}/debian-openrc-build.XXXXXXXX")"
STAGING="$(mktemp -d "$ROOT/build/output.XXXXXXXX")"
cp -a -- "$ROOT/auto" "$ROOT/config" "$WORKDIR/"
cd -- "$WORKDIR"
printf '%s\n' 'Configuring Debian Live build...'
lb config
printf '%s\n' 'Building the image; live-build needs elevated privileges...'
if (( EUID == 0 )); then
    lb build
else
    sudo lb build
fi

mapfile -t images < <(find "$WORKDIR" -maxdepth 1 -type f -name '*.hybrid.iso' -print)
if (( ${#images[@]} != 1 )); then
    printf 'Expected exactly one hybrid ISO; found %d. No release artifact was copied.\n' "${#images[@]}" >&2
    exit 1
fi

PACKAGE_LIST="$STAGING/$PACKAGE_BASENAME"
if (( EUID == 0 )); then
    chroot "$WORKDIR/chroot" dpkg-query -W -f='${binary:Package}\t${Version}\t${source:Package}\n' > "$PACKAGE_LIST"
else
    sudo chroot "$WORKDIR/chroot" dpkg-query -W -f='${binary:Package}\t${Version}\t${source:Package}\n' > "$PACKAGE_LIST"
fi
LC_ALL=C sort -o "$PACKAGE_LIST" "$PACKAGE_LIST"
cp -- "${images[0]}" "$STAGING/$BASENAME"

HOST_PRETTY_NAME=unknown
HOST_CODENAME=unknown
if [[ -r /etc/os-release ]]; then
    # Source trusted host metadata in a subprocess so it cannot replace VERSION.
    read_host_release() {
        . /etc/os-release
        printf '%s\n%s\n' "${PRETTY_NAME:-unknown}" "${VERSION_CODENAME:-unknown}"
    }
    mapfile -t host_release < <(read_host_release)
    HOST_PRETTY_NAME="${host_release[0]:-unknown}"
    HOST_CODENAME="${host_release[1]:-unknown}"
fi
BUILD_FINISHED_UTC="$(date -u +'%Y-%m-%dT%H:%M:%SZ')"
{
    printf 'project_version=%s\n' "$VERSION"
    printf 'target_distribution=Debian\n'
    printf 'target_suite=trixie\n'
    printf 'target_architecture=amd64\n'
    printf 'requested_init=/usr/sbin/openrc-init\n'
    printf 'source_ref=%s\n' "$SOURCE_REF"
    printf 'source_revision=%s\n' "$SOURCE_REVISION"
    printf 'builder_distribution=%s\n' "$HOST_PRETTY_NAME"
    printf 'builder_codename=%s\n' "$HOST_CODENAME"
    printf 'builder_kernel=%s\n' "$(uname -r)"
    printf 'live_build_version=%s\n' "$(lb --version 2>&1 | head -n 1)"
    printf 'build_started_utc=%s\n' "$BUILD_STARTED_UTC"
    printf 'build_finished_utc=%s\n' "$BUILD_FINISHED_UTC"
    printf 'package_inventory=%s\n' "$PACKAGE_BASENAME"
    printf 'reproducibility_status=not-established\n'
} > "$STAGING/$INFO_BASENAME"
(
    cd -- "$STAGING"
    sha256sum -- "$BASENAME" "$PACKAGE_BASENAME" "$INFO_BASENAME" > "$SUMS_BASENAME"
)

mkdir -p -- "$OUT"
# Staging is under the repository, so each rename is on the same filesystem.
mv -- "$STAGING/$BASENAME" "$OUT/$BASENAME"
mv -- "$STAGING/$PACKAGE_BASENAME" "$OUT/$PACKAGE_BASENAME"
mv -- "$STAGING/$INFO_BASENAME" "$OUT/$INFO_BASENAME"
mv -- "$STAGING/$SUMS_BASENAME" "$OUT/$SUMS_BASENAME"
printf 'ISO: %s\nPackage inventory: %s\nBuild information: %s\nChecksums: %s\n' \
    "$OUT/$BASENAME" "$OUT/$PACKAGE_BASENAME" "$OUT/$INFO_BASENAME" "$OUT/$SUMS_BASENAME"
printf '%s\n' 'Build success does not prove boot or installation; follow the QEMU test plan.'
