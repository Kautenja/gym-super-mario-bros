"""This module does setup for the notebooks in this directory."""
from os.path import abspath, join
from sys import path
# generate the new path to append to PATH (so we can import packages from
# the parent directory where `src` is)
module_path = abspath(join('..'))
# check if the path already exists
if module_path not in path:
    # add the new path to the python path
    path.append(module_path)
