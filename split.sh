#!/bin/bash -eu
cd "$(dirname "${BASH_SOURCE[0]}")"

blender -P split.py
