"""Local NxNative survey/build launcher. No game data is uploaded."""
import argparse
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
UPSTREAM = "https://github.com/seedds/nxnative.git"

def command(repo, game, keys, mode):
    script = repo / "scripts/build_ipa_from_nsp.py"
    if not script.is_file():
        raise ValueError("NxNative is missing; run: python3 arceus.py setup")
    if not game.is_dir() or not any(p.suffix.lower() == ".nsp" for p in game.iterdir()):
        raise ValueError("Game folder must contain your base-game NSP (and optional matching update).")
    if not keys.is_file():
        raise ValueError("Supply the path to your own prod.keys.")
    args = [sys.executable, str(script), str(game.resolve()), "-k", str(keys.resolve())]
    if mode == "survey":
        args += ["--survey-only"]
    else:
        args += ["--platform", "ios", "--app-name", "Pokemon Legends Arceus"]
        if mode == "xcode":
            args += ["--prepare-xcode"]
    return args

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("setup", help="Download the pinned NxNative source")
    build = sub.add_parser("run", help="Survey or attempt an experimental iPhone build")
    build.add_argument("--game", required=True, type=Path)
    build.add_argument("--keys", required=True, type=Path)
    build.add_argument("--mode", choices=["survey", "ipa", "xcode"], default="survey")
    options = parser.parse_args()
    repo = ROOT / "vendor/nxnative"
    pin = (ROOT / "nxnative.lock").read_text().strip()
    try:
        if options.action == "setup":
            if repo.exists():
                raise ValueError("vendor/nxnative already exists; preserving it. Verify its revision before use.")
            repo.parent.mkdir(exist_ok=True)
            subprocess.run(["git", "clone", "--no-checkout", UPSTREAM, str(repo)], check=True)
            subprocess.run(["git", "-C", str(repo), "checkout", "--detach", pin], check=True)
            print("Source ready. Install dependencies from vendor/nxnative/README.md on your Mac.")
            return 0
        if platform.system() != "Darwin":
            raise ValueError("Survey and iOS builds require macOS with Xcode; Windows can run the wrapper tests.")
        actual = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
        if actual != pin:
            raise ValueError("NxNative revision differs from nxnative.lock.")
        args = command(repo, options.game, options.keys, options.mode)
        print("Experimental Arceus workflow: a successful build does not establish playability.", flush=True)
        return subprocess.run(args, cwd=repo).returncode
    except (ValueError, OSError, subprocess.CalledProcessError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
