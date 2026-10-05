# Repository layout and boundaries

Build-time configuration (`auto/`, `config/`) is distinct from runtime system policy (`system/`), installer logic (`installer/`), original executable source (`src/`), third-party records (`third-party/`, `THIRD_PARTY.md`), and distribution identity (`configs/branding/`, `assets/branding/`).

`build/`, `dist/`, live-build work trees, caches, logs, and images are generated and ignored. Do not commit them. The project name is provisional and build-time text branding exists, but official artwork and logo assets remain unselected; required Debian provenance is retained. Empty subsystem directories contain a short boundary note rather than fake implementation code.
