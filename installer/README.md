# Installer boundary

No installer is implemented yet. The target design separates a small, testable installation engine from any TUI/GUI frontend. The engine must expose explicit disk selection, partition/filesystem plans, user/hostname/locale/timezone/keyboard configuration, bootloader installation, and profile selection.

Disk operations must be plan-first: show the exact target and changes, require an explicit confirmation, and never auto-select or erase a disk. Unit tests must use mocks or disposable disk images; QEMU tests must attach only a newly created disposable image. A future TUI must call the same engine rather than embedding storage logic in UI code.
