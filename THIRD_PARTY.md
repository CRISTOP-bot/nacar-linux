# Third-party components and attribution

No third-party source code, binary package, logo, font, or artwork is vendored in this repository at this stage. The project consumes upstream Debian packages through Debian's configured signed APT repositories during image construction; it does not claim ownership of those works.

## Components used by the bootstrap

| Component | Version | Origin | License / copyright | Modifications | Project location / use |
| --- | --- | --- | --- | --- | --- |
| Debian GNU/Linux archive packages | Exact versions are resolved at build time; see the generated `*.packages.tsv` next to each ISO | Debian archive selected by `auto/config` | Per-package copyright and licensing are supplied in the installed package's `/usr/share/doc/<package>/copyright`; see Debian's package metadata | None to upstream package sources in this repository | Installed into the generated live filesystem; requested package names are listed in `config/package-lists/base.list.chroot` |
| `live-build` | Exact version is recorded per image in its `.build-info.txt`; not pinned as a build input yet | Debian archive on the build host | Debian package copyright file `/usr/share/doc/live-build/copyright`; Debian Live manual is GPL-3-or-later | No upstream source changes; project-specific options live in `auto/config` | Build-time only |
| live-build bootloader templates | Copied at build time from `/usr/share/live/build/bootloaders` supplied by the installed `live-build` package | Debian archive on the build host | The upstream package and template notices remain applicable; copyright/comment lines are retained unmodified | `scripts/brand_bootloaders.py` changes visible menu directives in a temporary copy only; it leaves legal notices and non-visible technical settings intact | Build-time only; generated ISO boot menus |
| OpenRC | Binary version resolved from Debian archive at build time; exact version appears in the generated package inventory | Debian archive; upstream project is OpenRC | Package copyright is in `/usr/share/doc/openrc/copyright` inside the image; Debian packaging may contain additional notices | No upstream source changes; PID 1 selection is configured as a kernel boot argument and remains to be boot-verified | Requested in the live filesystem through the base package list |
| `actions/checkout` | v4.2.2, pinned to commit `11bd71901bbe5b1630ceea73d27597364c9af683` | `https://github.com/actions/checkout` | MIT License per upstream repository | Not modified | GitHub Actions workflows only; not included in the distribution image |


This table is a build policy, not a substitute for the actual release inventory. Before publishing an image, archive its package inventory and inspect each included package's copyright metadata. Where source redistribution obligations apply, provide corresponding source and notices as required by the component's license. Do not infer one license for all Debian packages.

## Per-build inventory

`build.sh` writes a tab-separated package/version/source inventory, a build-information file (target, source ref/revision when supplied, host distribution, kernel, `live-build` version, timestamps, and reproducibility status), and a SHA-256 file beside the ISO. These artifacts are generated locally and ignored by Git. They record the binary package set and builder context; they are not a complete license scan and do not replace upstream copyright files or required source distribution.

## Before adding a dependency

1. Identify the canonical upstream and exact version/revision.
2. Read the upstream and Debian packaging copyright/license metadata.
3. Check compatibility with the intended distribution and redistribution model.
4. Preserve notices and source offers as required.
5. Record version, origin, license, copyright, modifications, and location here.
6. Stop and document the issue if provenance or license terms are unclear or incompatible.
