# GitHub-hosted Mac testing

The GitHub Mac tests workflow runs automatically on main and can also be started from Actions > GitHub Mac tests > Run workflow.

It uses the same xcode-27 runner and Xcode 27.1 path as the pinned NxNative upstream CI. Apple compilation tools are installed on GitHub's Mac; you do not need a local Mac or Xcode installation for these tests.

Two jobs run:
- Mac runtime unit tests and CPU texture layout/deswizzle tests.
- iPhone SDK source compilation and linking an unsigned synthetic iOS app.

Tests use upstream's Wonder profile as a runtime fixture because the pinned source has no verified Arceus profile. The synthetic app contains no game, cannot play Arceus, and is intentionally not offered as an installable release. Logs are saved as Actions artifacts for seven days.

GitHub's virtual Mac runners lack the Metal GPU support required by NxNative's graphics runtime, according to upstream CI. These jobs can check compilation and CPU behavior; they cannot establish game rendering or playability.

The actual Arceus survey/build still requires your base NSP and own keys. No remote game upload or credential handling has been configured. Signing and sideloading an eventual game IPA is a separate step.
