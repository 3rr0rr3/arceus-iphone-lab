# Arceus iPhone Lab

Experimental local build launcher for [NxNative](https://github.com/seedds/nxnative), pinned in nxnative.lock. The goal is to run a personally supplied Pokémon Legends: Arceus dump directly on iPhone.

**Status: no Arceus boot, graphics, performance, or iPhone installation has been verified.** This repository adds orchestration and tests, not a completed Arceus port. A packaged IPA can still fail to launch. NxNative uses code rewriting, a Horizon service host, and graphics translation to Metal.

## Start on a Mac

Install Git and Python 3.12 or newer, then:

```sh
git clone https://github.com/3rr0rr3/arceus-iphone-lab.git
cd arceus-iphone-lab
python3 arceus.py setup
```

Follow vendor/nxnative/README.md to install the pinned version's Xcode, Metal compiler, Python and other build dependencies. The reviewed revision specifies Xcode 27.1; use its own instructions as the authority. Building and surveying require macOS; the Windows machine used to create this repository cannot compile an iOS IPA.

Keep your base NSP and optional matching update in a local folder outside this checkout. Keep your own prod.keys local too. Do not put these files in issues, releases, Actions inputs, or artifacts.

```sh
python3 arceus.py run --game "/path/to/Arceus" --keys "/path/to/prod.keys"
```

The default mode surveys the game without attempting packaging. Review the generated 01001F5010DFA000_survey/survey.md in the game folder. Confirm the identified title ID is 01001F5010DFA000 before continuing; the launcher delegates game identification to NxNative.

Then try an experimental unsigned IPA:

```sh
python3 arceus.py run --game "/path/to/Arceus" --keys "/path/to/prod.keys" --mode ipa
```

For device signing and installation through Xcode:

```sh
python3 arceus.py run --game "/path/to/Arceus" --keys "/path/to/prod.keys" --mode xcode
```

Open the generated project, select your development team and connected iPhone, and build/run. Alternatively sign the generated IPA with your existing sideloading tool. Neither automatic signing nor device installation is implemented by this wrapper. NxNative documents iOS 26 and A17 Pro or newer devices, plus increased-memory-limit signing for memory-heavy games; Arceus-specific memory requirements are unmeasured.

## Tests and next experiments

```sh
python3 -m unittest discover -s tests -v
```

GitHub Actions tests input validation and command construction, fetches the exact upstream commit, parses its builder, checks required option strings, and reports whether an Arceus profile exists. It does not execute the game or compile an IPA.

Next milestones: local survey; resolve startup failures from local logs; verify title screen and a new save; validate rendering, controls, audio, save/load, and sleep/resume on an iPhone. Record game version, upstream SHA, device and iOS version with each result. Review logs before sharing any excerpts.

Reference: [Arceus discussion #162](https://github.com/seedds/nxnative/issues/162). This is a proposed Mac workflow, not proof of iPhone playability.

## Licensing

The original launcher and tests here are MIT licensed; see LICENSE. NxNative and its dependencies retain their own licenses. No game content, keys, firmware, or Nintendo code is distributed here.
