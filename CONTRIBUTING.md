# Contributing To gym-super-mario-bros

Help improve the environments through bug reports, documentation, tests, and
code. This guide covers setup, architecture, validation, and the compatibility
requirements used in review.

- [Set up your environment](#set-up-your-environment)
- [Understand the architecture](#architecture)
- [Develop and test](#development-and-testing)
- [Choose validation for your change](#choosing-validation)
- [Prepare a release](#prepare-a-release)
- [Submit a pull request](#submit-a-pull-request)

## Before You Start

Search the [existing issues][issues] before reporting a bug or proposing a
feature. Include the operating system and CPU architecture, Python version,
`gym-super-mario-bros`, `nes-py`, and Gymnasium versions, installation commands,
and a minimal reproduction. For gameplay problems, include the environment ID,
seed, action sequence or policy, wrappers, render mode, and expected versus
observed behavior. Include a traceback for exceptions and screenshots when
they help explain a rendering problem. Discuss substantial API or environment
behavior changes in an issue before starting.

Read the [README](README.md), [changelog](CHANGELOG.md), and
[licensing guide](LICENSING.md). Original code uses the [MIT License](LICENSE);
the Nintendo ROM assets are excluded from that grant. Preserve that distinction
when changing assets or packaging.
Follow the [Google Python Style Guide][python-style] referenced by the
[pull request template](.github/PULL_REQUEST_TEMPLATE.md), while keeping edits
consistent with nearby code. Preserve existing attribution and license notices.

## Set Up Your Environment

Use Git and CPython 3.13 or newer. CI currently tests Python 3.13 and 3.14.
The `nes-py` dependency contains native code; building it from source requires
a compatible C++ toolchain. See the [nes-py installation notes][nes-py-install]
for platform requirements and native-library troubleshooting. Human keyboard
play requires a graphical desktop session. Markdown-only changes do not
require installing the emulator.

### Get The Source

Fork the repository on GitHub for a pull request and substitute your fork's
URL in the clone command:

```shell
git clone https://github.com/Kautenja/gym-super-mario-bros.git
cd gym-super-mario-bros
git switch -c docs/contributor-setup
```

Choose a branch name describing your change. Run the remaining commands from
the repository root unless stated otherwise.

### Install For Development

On macOS or Linux, the [main.sh](main.sh) helper creates `.venv` and installs
the package in editable mode:

```shell
PYTHON=python3.13 ./main.sh install
./main.sh python
```

You can substitute `python3.14`. An existing `.venv/bin/python` takes
precedence over `PYTHON`; check the printed interpreter when switching Python
versions. The helper does not activate the environment in your shell.

The equivalent setup without the Bash helper is:

```shell
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

For Windows PowerShell, create and activate the environment with:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

Use the direct `python -m ...` commands below in an activated environment.
The Bash helper expects a Unix-style `.venv/bin/python` layout.

[pyproject.toml](pyproject.toml) owns runtime dependencies and package metadata.
[requirements.txt](requirements.txt) bootstraps developer and CI tools. When
working on emulator changes too, keep a `nes-py` checkout at `../nes-py` and run
`./main.sh install-local` to install both projects in editable mode. That
command falls back to the declared dependency if the sibling is absent. Record
the emulator commit when reporting results from a local dependency checkout.

## Architecture

- `gym_super_mario_bros/__init__.py` exposes the public API and imports
  `_registration.py`, which registers environments and aliases with Gymnasium.
- `smb_env.py` implements Super Mario Bros. and Lost Levels. `smb2_env.py`
  implements Super Mario Bros. 2 (USA), and `smb3_env.py` implements Super Mario
  Bros. 3. These classes build on `nes_py.NESEnv` and interpret game RAM for
  reset entry points, rewards, termination, and `info` fields.
- `gym_super_mario_bros/_roms/` contains packaged ROM assets, path resolution,
  and target decoding. `pyproject.toml` declares the ROM package data.
- `tasks.py` defines `MarioTask` and the queryable task inventory.
  `smb3_stages.py` separates the numbered-course catalog from validated SMB3
  reset entry points. A catalog entry alone does not establish a playable,
  registered single-stage environment.
- `actions.py` supplies action presets for `nes_py.wrappers.JoypadSpace`.
  `_app/cli.py` implements keyboard and random play.
- `gym_super_mario_bros/tests/` contains `unittest` regression and emulator
  smoke tests. `main.sh` supplies local setup, test, and build shortcuts.

Paths without the package prefix above are inside `gym_super_mario_bros/`.
Keep CPU, PPU, mapper, and native rendering fixes in the upstream [nes-py]
project when they concern the emulator itself. Keep game-specific RAM decoding
and reinforcement-learning behavior in this wrapper package.

### Compatibility And Behavior

Preserve the Gymnasium contract: `reset()` returns `(observation, info)`, and
`step()` returns `(observation, reward, terminated, truncated, info)`.
Choose rendering through `render_mode` at construction. Registered environments
use Gymnasium's `TimeLimit`; external step limits produce truncation, while
game events determine termination. Check full-game and single-stage behavior
separately, including life loss, game over, and completion.

Environment IDs, aliases, action ordering, canonical task IDs, and `info` keys
are used by training code and published experiments. Coordinate changes across
registration, task metadata, tests, README examples, and the changelog. Explain
intentional compatibility changes explicitly. Registration disables Gymnasium's
passive checker, so retain direct reset, step, render, and wrapper coverage.

Reward changes affect comparisons with earlier experiments. Verify component
values, clipping, reset of accumulated state, and the diagnostic `info` fields.
For RAM and stage-entry changes, document the game, addresses, observed states,
and a reproducible action sequence. Validate new SMB3 entry recipes before
marking stages as validated or registering them.

## Development And Testing

Run the full suite with either the helper or the equivalent direct command:

```shell
./main.sh test
```

```shell
python -m unittest discover .
```

For a focused check in an activated environment:

```shell
python -m unittest gym_super_mario_bros.tests.test_smb3_env
```

Use the corresponding module for your change. `test_smv_env` covers SMB1 and
Lost Levels; `test_smb2_env` covers SMB2 USA. Registration, task metadata, ROM
paths, and CLI behavior have separate test modules. The suite includes actual
emulator construction and stepping against packaged assets as well as mocked
CLI checks and controlled RAM-state regressions. It does not require human
keyboard play, and passing it does not establish that every stage or gameplay
sequence works.

Add focused regressions for behavior changes and reproduce bugs before fixing
them where practical. Keep fixtures and action sequences repeatable, avoid
depending on wall-clock timing, and close environments after use.

For a headless smoke run or interactive keyboard check:

```shell
./main.sh random --env SuperMarioBros-v0 --steps 1000 --no-render --seed 123
./main.sh cli --env SuperMarioBros-v0 --mode human --actionspace simple
```

With an activated environment, replace `./main.sh random` with
`gym_super_mario_bros --mode random`, or `./main.sh cli` with
`gym_super_mario_bros`. Select the affected game and stage for your change.

Build source and wheel distributions with:

```shell
python -m build
```

Outputs go to `dist/`. `./main.sh build` cleans build outputs first, then builds;
`./main.sh ship` runs tests and that clean build. The `release` and `upload`
aliases also only test and build locally. Preserve any experiment artifacts
you need before running the helper's cleanup commands.

### Continuous Integration

The [CI workflow](.github/workflows/ci.yml) installs dependencies and the package,
runs `python -m unittest discover .`, and builds distributions on Python 3.13
and 3.14 across Linux x64/arm64, macOS x64/arm64, and Windows x64. It runs on
pull requests, pushes to `master`, and tag pushes. Feature-branch pushes alone
do not trigger this workflow. Tag builds also create or update a GitHub release
and attach distribution artifacts after the test matrix succeeds.

### Choosing Validation

| Change | Relevant Validation |
| --- | --- |
| Markdown guidance | Check links, paths, commands, and the complete diff; run `git diff --check` |
| Game RAM, rewards, or termination | Run affected game tests and the full suite; exercise the relevant gameplay, reset, life-loss, and completion sequence |
| Registration or task inventory | Run registration and task tests; check aliases, canonical IDs, stage filters, and wrapper behavior |
| CLI or action presets | Run CLI tests and affected environment tests; check headless random play and graphical keyboard play where relevant |
| Rendering | Run affected frame regressions and inspect actual graphical output |
| Dependencies or packaging | Run the full suite and build distributions; install a wheel in a fresh environment and smoke-test from outside the source checkout |

Record the commands, dependency versions, environment IDs, and results. State
skipped checks and failures. For performance claims, compare repeated runs of
the same workload, render mode, action sequence, and dependency versions.

## Prepare A Release

Align the version in `pyproject.toml` and `CITATION.cff`, update `CHANGELOG.md`,
and revise affected README examples. Preserve the original 2018 preferred
citation across [CITATION.cff](CITATION.cff), [CITATION.bib](CITATION.bib), and
the [README citation](README.md#citation); a new software release does not
change that citation's title, author, or year.

Run the full suite, build distributions, and verify CI on the intended release
commit. Inspect package contents and test an installed wheel independently of
the source checkout. Create a new tag matching the package version, optionally
prefixed with `v`. Do not move an already published tag to include a fix.

PyPI publication uses the separate
[Publish to PyPI workflow](.github/workflows/publish.yml), triggered by a
published GitHub release or a manual dispatch on a tag. Its version check
rejects branch runs and tags that
do not match `pyproject.toml`. The `pypi` GitHub environment and PyPI trusted
publisher must be configured as described in the [README](README.md#publishing).
Check that the publishing workflow actually ran; if needed, dispatch it on the
version-matching tag. Verify the resulting PyPI version and artifacts before
announcing availability. A successful local build or CI artifact upload alone
does not confirm PyPI publication.

## Submit A Pull Request

1. Keep each contribution focused. Update tests and documentation alongside
   behavior changes, and avoid unrelated formatting or dependency upgrades.
2. Review the intended files from the repository root:

   ```shell
   git diff --check
   git diff
   git status --short
   ```

3. Commit the intended files, push your branch to your fork, and open a pull
   request against `master` using the repository's template. Describe the
   problem, resulting behavior, related issue, and compatibility effects.
4. Include validation commands and results, relevant platform and dependency
   versions, and any skipped checks or unresolved failures. Include screenshots
   for visible changes and reproducible gameplay details for environment fixes.

[issues]: https://github.com/Kautenja/gym-super-mario-bros/issues
[python-style]: https://google.github.io/styleguide/pyguide.html
[nes-py]: https://github.com/Kautenja/nes-py
[nes-py-install]: https://github.com/Kautenja/nes-py#installation
