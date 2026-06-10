# Changelog

This changelog is reconstructed from the repository's local tags, README,
package metadata, and commit history.

## 8.0.0 (Unreleased)

Upcoming major release aligned with the current `pyproject.toml` version.

- Breaking changes:
  - Migrated the package from the legacy Gym API to Gymnasium.
  - Raised the minimum Python version to 3.13.
  - Raised the runtime dependency floor to `gymnasium>=1.0.0` and
    `nes-py>=9.0.0`.
- Packaging and publishing:
  - Replaced the legacy `setup.py`-first packaging flow with modern
    `pyproject.toml` metadata.
  - Added a trusted-publishing PyPI workflow and documented the release flow
    around GitHub tags and releases.
- Tooling and maintenance:
  - Moved CI from Travis CI to GitHub Actions and added Python 3.14 parity.
  - Replaced the old `makefile` workflow with `main.sh`.
  - Clarified wrapper bootstrap metadata and refreshed README usage guidance.
- Environments:
  - Added vanilla Super Mario Bros. 2 (USA) support through
    `SuperMarioBros2USA-v0` and 20 single-stage
    `SuperMarioBros2USA-<world>-<stage>-v0` environments.
  - Added vanilla Super Mario Bros. 3 support through `SuperMarioBros3-v0`
    and the validated `SuperMarioBros3-1-1-v0` single-stage environment.
  - Enriched SMB1, SMB2 USA, and SMB3 info dictionaries and expanded reward
    shaping beyond raw rightward velocity.

## 7.4.0 (2022-06-20)

- Added random-stage subset support so callers can limit the stage pool for
  `SuperMarioBrosRandomStages-*` environments.
- Updated the CLI to support random-stage environment workflows.
- Documented the random-stage feature set in the README.
- Fixed a `np.bool` compatibility issue and removed code that became redundant
  after newer `nes-py` behavior.

## 7.3.x (2019-09-28 to 2022-06-06)

- Refined Python 3 support and updated package classifiers.
- Bumped the `nes-py` dependency to newer 8.x releases.
- Tightened CI and packaging metadata for PyPI distribution.
- Refreshed README and project metadata for publishing compatibility.

Tags in this line: `7.3.0`, `7.3.1`, `7.3.2`, `7.3.3`.

## 7.2.x (2019-04-30 to 2019-06-02)

- Added `y_pos` to the `info` dictionary and documented it in the README.
- Simplified environment status helpers and improved `is_stage_over`.
- Polished CLI, setup metadata, and README details.

Tags in this line: `7.2.0`, `7.2.1`, `7.2.2`, `7.2.3`.

## 7.1.x (2019-01-16 to 2019-01-21)

- Introduced the random-level environment family.
- Contained RNG handling within the environment and fixed related seeding
  behavior.
- Added `get_action_meanings`.
- Removed an older CLI wrap feature and aligned with newer `nes-py` behavior.

Tags in this line: `7.1.0`, `7.1.1`, `7.1.2`, `7.1.3`, `7.1.4`, `7.1.5`,
`7.1.6`.

## 7.0.x (2019-01-06)

- Simplified the package surface and removed deprecated environments and
  deprecated functionality.
- Updated the CLI to match newer `nes-py` command-line behavior.
- Fixed registration coverage around the streamlined environment set.

Tags in this line: `7.0.0`, `7.0.1`.

## 6.x and earlier (2018 to early 2019)

- Established the initial Super Mario Bros. Gym wrapper releases, ROM-backed
  environment variants, CLI support, and early packaging cadence.
- Published many fast-follow patch releases while stabilizing gameplay APIs,
  registration, and distribution.
