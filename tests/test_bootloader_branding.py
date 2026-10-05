# SPDX-License-Identifier: GPL-3.0-or-later
import tempfile
import unittest
from pathlib import Path

from scripts.brand_bootloaders import brand_bootloaders


class BootloaderBrandingTests(unittest.TestCase):
    def test_visible_labels_are_nacar_and_comments_are_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            isolinux = root / "isolinux" / "menu.cfg"
            grub = root / "grub" / "grub.cfg"
            legal = root / "isolinux" / "COPYING"
            isolinux.parent.mkdir(parents=True)
            grub.parent.mkdir(parents=True)
            isolinux.write_text(
                "# Copyright Debian Live contributors\n"
                "menu title Debian GNU/Linux Live\n"
                "label live\n menu label ^Debian GNU/Linux Live\n"
                "set upstream_name=Debian\n",
                encoding="utf-8",
            )
            grub.write_text(
                "# Debian notice remains intact\n"
                "menuentry 'Debian GNU/Linux Live (amd64)' --id live {\n"
                "    linux /live/vmlinuz boot=live\n"
                "}\n",
                encoding="utf-8",
            )
            legal.write_text("Debian Live upstream copyright text\n", encoding="utf-8")

            changed = brand_bootloaders(root)

            self.assertEqual(changed, 3)
            self.assertIn("menu title Nacar GNU/Linux Live", isolinux.read_text())
            self.assertIn("menu label ^Nacar GNU/Linux Live", isolinux.read_text())
            self.assertIn("set upstream_name=Debian", isolinux.read_text())
            self.assertIn("menuentry 'Nacar GNU/Linux Live (amd64)'", grub.read_text())
            self.assertIn("# Copyright Debian Live contributors", isolinux.read_text())
            self.assertIn("# Debian notice remains intact", grub.read_text())
            self.assertIn("Debian Live upstream copyright text", legal.read_text())

    def test_missing_template_directory_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                brand_bootloaders(Path(tmp) / "missing")


if __name__ == "__main__":
    unittest.main()
