# Repository layout and boundaries

Build-time configuration (`auto/`, `config/`) is distinct from runtime system policy (`system/`), installer logic (`installer/`), original executable source (`src/`), third-party records (`third-party/`, `THIRD_PARTY.md`), and distribution identity (`configs/branding/`, `assets/branding/`).

`build/`, `dist/`, live-build work trees, caches, logs, and images are generated and ignored. Do not commit them unless a narrowly documented release artifact policy is introduced. Branding files are intentionally absent until a distinct name and permissions are selected. Empty subsystem directories contain a short boundary note rather than fake implementation code.
