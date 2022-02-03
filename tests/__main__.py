import unittest
from pm2py import PM2


class TestPM2(unittest.TestCase):
    def test_start_script(self):
        return self.assertEqual(PM2().start("tests/test_script.sh", ["-f"]), True)

    def test_start_script_with_args(self):
        return self.assertEqual(PM2().start("tests/test_script2.sh", ["--name", "test_script2", "-f"]), True)

    def test_list_processes_count(self):
        return self.assertEqual(len(PM2().list()), 2)

    def test_list_processes_stopped(self):
        return self.assertEqual(PM2().list()[0].mode, "stopped")

    def test_stop_script_name(self):
        return self.assertEqual(PM2().stop("test_script2"), True)

    def test_restart_script_name(self):
        return self.assertEqual(PM2().restart("test_script2"), True)

    def test_stop_script_all(self):
        return self.assertEqual(PM2().stop("all"), True)


if __name__ == '__main__':
    unittest.main()
