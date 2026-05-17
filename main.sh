#!/bin/bash
#
# Usage:
#     ./main.sh [options] [command] [args...]
#
# Options:
#     -h    Print documentation about this script
#
# Commands:
#     python              Print the Python interpreter used by this project
#     install             Create/use .venv and install project dependencies
#     install-local       Install sibling ../nes-py first, then this package
#     unittest            Execute the unit test suite
#     test                Alias for unittest
#     clean               Remove build artifacts and Python bytecode
#     deployment          Clean, then build source and wheel distributions
#     build               Alias for deployment
#     dist                Alias for deployment
#     package             Alias for deployment
#     ship                Run tests, build distributions, then upload to PyPI
#     release             Alias for ship
#     upload              Alias for ship
#     all                 Run tests and build distributions
#     cli                 Run the package CLI; pass extra args after the command
#     play                Alias for cli
#     random              Run the package CLI in random mode
#     speedtest           Run the legacy speedtest.py script
#     *                   Execute the command directly from the project root
#
# Examples:
#     ./main.sh install-local
#     ./main.sh test
#     ./main.sh deployment
#     ./main.sh cli --env SuperMarioBros-v0 --actionspace simple
#     ./main.sh random --env SuperMarioBros-v0 --steps 100
#     ./main.sh speedtest
#

set -euo pipefail

print_help() {
  sed -ne '/^#/!q;s/.\{1,2\}//;1d;p' < "$0"
}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

if [[ -x "${SCRIPT_DIR}/.venv/bin/python" ]]; then
  PYTHON="${SCRIPT_DIR}/.venv/bin/python"
else
  PYTHON="${PYTHON:-python3}"
fi

while getopts ":h" optname; do
  case "$optname" in
  "h")
    print_help
    exit 0
    ;;
  "?")
    echo "Unknown option ${OPTARG}" >&2
    exit 1
    ;;
  ":")
    echo "No argument value for option ${OPTARG}" >&2
    exit 1
    ;;
  *)
    echo "Unknown error while processing options" >&2
    exit 1
    ;;
  esac
done

shift $((OPTIND - 1))

COMMAND="${1:-}"
if [[ $# -gt 0 ]]; then
  shift
fi

ensure_venv() {
  if [[ ! -x "${SCRIPT_DIR}/.venv/bin/python" ]]; then
    echo "Creating ${SCRIPT_DIR}/.venv"
    if ! "${PYTHON}" -m venv "${SCRIPT_DIR}/.venv"; then
      echo "Failed to create .venv. Install python3-venv if your platform splits it out." >&2
      exit 1
    fi
  fi
  PYTHON="${SCRIPT_DIR}/.venv/bin/python"
}

run_install() {
  ensure_venv
  "${PYTHON}" -m pip install --upgrade pip
  if [[ -f requirements.txt ]]; then
    "${PYTHON}" -m pip install -r requirements.txt
  fi
  "${PYTHON}" -m pip install -e .
}

run_install_local() {
  ensure_venv
  "${PYTHON}" -m pip install --upgrade pip
  "${PYTHON}" -m pip install "build>=1.2.1" "PyYAML>=6.0.2"
  if [[ -d "${SCRIPT_DIR}/../nes-py" ]]; then
    "${PYTHON}" -m pip install -e "${SCRIPT_DIR}/../nes-py"
  fi
  "${PYTHON}" -m pip install -e .
}

run_clean() {
  rm -rf build/ dist/ .eggs/ *.egg-info/
  find . -path "./.venv" -prune -o -type f -name "*.pyc" -exec rm -f {} +
  find . -path "./.venv" -prune -o -type d -name "__pycache__" -prune -exec rm -rf {} +
}

run_unittest() {
  "${PYTHON}" -m unittest discover . "$@"
}

run_deployment() {
  run_clean
  "${PYTHON}" -m build
}

run_ship() {
  run_unittest
  run_deployment
  "${PYTHON}" -m pip install ".[release]"
  "${PYTHON}" -m twine upload dist/*
}

case "${COMMAND}" in

"")
  print_help
  exit 0
  ;;

"python")
  echo "${PYTHON}"
  exit 0
  ;;

"install")
  run_install
  exit 0
  ;;

"install-local")
  run_install_local
  exit 0
  ;;

"unittest" | "test")
  run_unittest "$@"
  exit 0
  ;;

"clean")
  run_clean
  exit 0
  ;;

"deployment" | "build" | "dist" | "package")
  run_deployment
  exit 0
  ;;

"ship" | "release" | "upload")
  run_ship
  exit 0
  ;;

"all")
  run_unittest
  run_deployment
  exit 0
  ;;

"cli" | "play")
  "${PYTHON}" -m gym_super_mario_bros._app.cli "$@"
  exit 0
  ;;

"random")
  "${PYTHON}" -m gym_super_mario_bros._app.cli --mode random "$@"
  exit 0
  ;;

"speedtest")
  "${PYTHON}" speedtest.py "$@"
  exit 0
  ;;

*)
  "${COMMAND}" "$@"
  exit 0
  ;;

esac
