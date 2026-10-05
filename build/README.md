# Build outputs

`build.sh` uses a fresh temporary directory on the host for `live-build`; it does not clean or reuse a previous working tree. This directory contains only this note in the source repository. `dist/` contains generated ISO, package inventory, and checksum outputs and is ignored by Git. Neither directory is source code. Do not delete or replace prior artifacts without checking their value.
