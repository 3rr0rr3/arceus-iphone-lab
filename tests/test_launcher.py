from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import arceus

class LauncherTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo = self.root / "source"
        (self.repo / "scripts").mkdir(parents=True)
        (self.repo / "scripts/build_ipa_from_nsp.py").touch()
        self.game = self.root / "Game with spaces"
        self.game.mkdir()
        (self.game / "base.nsp").touch()
        self.keys = self.root / "prod.keys"
        self.keys.write_text("test fixture only")

    def test_survey_is_separate_from_packaging(self):
        args = arceus.command(self.repo, self.game, self.keys, "survey")
        self.assertIn("--survey-only", args)
        self.assertNotIn("--platform", args)
        self.assertIn(str(self.game.resolve()), args)

    def test_ipa_and_xcode_modes(self):
        for mode in ("ipa", "xcode"):
            args = arceus.command(self.repo, self.game, self.keys, mode)
            self.assertEqual(args[args.index("--platform") + 1], "ios")
            self.assertEqual("--prepare-xcode" in args, mode == "xcode")

    def test_missing_keys_stops_before_execution(self):
        with self.assertRaises(ValueError):
            arceus.command(self.repo, self.game, self.root / "missing.keys", "ipa")

    def test_empty_game_folder_rejected(self):
        empty = self.root / "empty"
        empty.mkdir()
        with self.assertRaises(ValueError):
            arceus.command(self.repo, empty, self.keys, "survey")

    def test_windows_rejected_before_upstream_execution(self):
        with patch("sys.argv", ["arceus.py", "run", "--game", "x", "--keys", "y"]), patch("arceus.platform.system", return_value="Windows"), patch("arceus.subprocess.run") as run:
            self.assertEqual(arceus.main(), 1)
            run.assert_not_called()

if __name__ == "__main__":
    unittest.main()
