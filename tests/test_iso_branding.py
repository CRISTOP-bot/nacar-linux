# SPDX-License-Identifier: GPL-3.0-or-later
import tempfile
import unittest
from pathlib import Path

from scripts.check_boot_branding import check_boot_configs
from scripts.check_iso_metadata import EXPECTED, FIELDS, SECTOR_SIZE, PVD_SECTOR, verify_iso


class IsoBrandingTests(unittest.TestCase):
    def test_iso_primary_volume_descriptor_has_nacar_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "nacar.iso"
            data = bytearray((PVD_SECTOR + 1) * SECTOR_SIZE)
            start = PVD_SECTOR * SECTOR_SIZE
            data[start] = 1
            data[start + 1 : start + 6] = b"CD001"
            data[start + 6] = 1
            for key, (offset, size) in FIELDS.items():
                value = EXPECTED[key].encode("ascii")
                data[start + offset : start + offset + size] = value.ljust(size, b" ")
            image.write_bytes(data)
            self.assertEqual(verify_iso(image), EXPECTED)

    def test_iso_metadata_rejects_debian_label(self):
        with tempfile.TemporaryDirectory() as tmp:
            image = Path(tmp) / "nacar.iso"
            data = bytearray((PVD_SECTOR + 1) * SECTOR_SIZE)
            start = PVD_SECTOR * SECTOR_SIZE
            data[start] = 1
            data[start + 1 : start + 6] = b"CD001"
            data[start + 6] = 1
            for key, (offset, size) in FIELDS.items():
                value = EXPECTED[key].encode("ascii")
                if key == "volume":
                    value = b"DEBIAN_LIVE"
                data[start + offset : start + offset + size] = value.ljust(size, b" ")
            image.write_bytes(data)
            with self.assertRaisesRegex(ValueError, "unexpected ISO volume field"):
                verify_iso(image)

    def test_extracted_boot_menus_must_be_nacar_branded(self):
        with tempfile.TemporaryDirectory() as tmp:
            isolinux = Path(tmp) / "isolinux"
            grub = Path(tmp) / "grub"
            isolinux.mkdir()
            grub.mkdir()
            (isolinux / "menu.cfg").write_text("menu title Nacar GNU/Linux Live\n", encoding="utf-8")
            (grub / "grub.cfg").write_text("menuentry 'Nacar GNU/Linux Live' {\n}\n", encoding="utf-8")
            self.assertEqual(check_boot_configs([isolinux, grub]), (2, 2))

    def test_extracted_boot_menus_reject_debian_branding(self):
        with tempfile.TemporaryDirectory() as tmp:
            isolinux = Path(tmp) / "isolinux"
            grub = Path(tmp) / "grub"
            isolinux.mkdir()
            grub.mkdir()
            (isolinux / "menu.cfg").write_text("menu title Nacar GNU/Linux Live\n", encoding="utf-8")
            (grub / "grub.cfg").write_text("menuentry 'Debian GNU/Linux Live' {\n}\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "Debian appears"):
                check_boot_configs([isolinux, grub])


if __name__ == "__main__":
    unittest.main()
