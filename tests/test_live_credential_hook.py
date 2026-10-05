# SPDX-License-Identifier: GPL-3.0-or-later
import os
import pathlib
import pty
import subprocess
import tempfile
import time
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
HOOK = ROOT / "config/includes.chroot/usr/lib/live/config-hooks/9999-nacar-live-credentials"
PASSWORD = "MFRGGZDFMZTWQ2LK"


class LiveCredentialHookTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="nacar-hook-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = pathlib.Path(self.temp.name)
        self.bin = self.root / "bin"
        self.bin.mkdir()
        self.capture = self.root / "chpasswd-input"
        self.script = self.root / "hook"

        source = HOOK.read_text()
        self.assertIn("LIVE_CONSOLE=/dev/console", source)
        self.script.write_text(source.replace("LIVE_CONSOLE=/dev/console", "LIVE_CONSOLE=__CONSOLE__"))
        self.script.chmod(0o755)
        self._write_command("id", """#!/bin/sh
[ \"${1:-}\" = -u ] || exit 2
printf '%s\\n' \"${TEST_UID:-0}\"
""")
        self._write_command("getent", """#!/bin/sh
case \"${1:-}\" in
  passwd)
    [ \"${TEST_NO_USER:-0}\" = 0 ] || exit 2
    printf 'live:x:1000:1000:Live:/home/live:/bin/bash\\n'
    ;;
  shadow)
    printf 'live:%s:20000:0:99999:7:::\\n' \"${TEST_OLD_HASH:-!locked}\"
    ;;
  *) exit 2 ;;
esac
""")
        self._write_command("dd", """#!/bin/sh
printf '1234567890'
""")
        self._write_command("base32", """#!/bin/sh
printf 'MFRGGZDFMZTWQ2LK\\n'
""")
        self._write_command("tr", """#!/bin/sh
exec /usr/bin/tr \"$@\"
""")
        self._write_command("chpasswd", """#!/bin/sh
input=$(cat)
printf '%s\\n' \"$input\" >> \"$TEST_CHPASS_CAPTURE\"
if [ \"${1:-}\" != --encrypted ] && [ \"${TEST_FAIL_SET:-0}\" = 1 ]; then
  exit 1
fi
exit 0
""")

    def _write_command(self, name, content):
        path = self.bin / name
        path.write_text(content)
        path.chmod(0o755)

    def _run(self, console=None, **extra_env):
        env = os.environ.copy()
        env.update({
            "PATH": f"{self.bin}:/usr/bin:/bin",
            "TEST_CHPASS_CAPTURE": str(self.capture),
            **extra_env,
        })
        master, slave = pty.openpty()
        if console is None:
            console = os.ttyname(slave)
        self.script.write_text(HOOK.read_text().replace("LIVE_CONSOLE=/dev/console", f'LIVE_CONSOLE="{console}"'))
        try:
            result = subprocess.run([str(self.script)], text=True, capture_output=True, env=env, timeout=10)
            os.close(slave)
            slave = -1
            console_output = bytearray()
            for _ in range(20):
                try:
                    console_output.extend(os.read(master, 4096))
                except BlockingIOError:
                    time.sleep(0.005)
                except OSError:
                    break
                if len(console_output) >= 4096:
                    break
            return result, console_output.decode(errors="replace")
        finally:
            if slave >= 0:
                os.close(slave)
            os.close(master)

    def test_success_sets_password_over_stdin_and_shows_only_on_console(self):
        result, output = self._run()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.capture.read_text(), f"live:{PASSWORD}\n")
        self.assertIn(PASSWORD, output)
        self.assertNotIn(PASSWORD, result.stdout + result.stderr)

    def test_missing_live_user_fails_before_password_change(self):
        result, output = self._run("/dev/pts/nonexistent", TEST_NO_USER="1")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("live account does not exist", result.stderr)
        self.assertNotIn(PASSWORD, result.stdout + result.stderr + output)
        self.assertFalse(self.capture.exists())

    def test_failed_password_change_restores_prior_hash_without_display(self):
        result, output = self._run("/dev/full", TEST_FAIL_SET="1", TEST_OLD_HASH="!locked")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.capture.read_text(), f"live:{PASSWORD}\nlive:!locked\n")
        self.assertNotIn(PASSWORD, output + result.stdout + result.stderr)

    def test_console_write_failure_restores_prior_hash(self):
        result, output = self._run("/dev/full", TEST_OLD_HASH="!locked")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.capture.read_text(), f"live:{PASSWORD}\nlive:!locked\n")
        self.assertNotIn(PASSWORD, output + result.stdout + result.stderr)

    def test_unavailable_console_fails_before_password_change(self):
        result, output = self._run("/no-such-nacar-console")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("local console is unavailable", result.stderr)
        self.assertNotIn(PASSWORD, output + result.stdout + result.stderr)
        self.assertFalse(self.capture.exists())


if __name__ == "__main__":
    unittest.main()
