#!/bin/bash -eux

cd "$(dirname "${BASH_SOURCE[0]}")"

cd textures

for f in *.jpeg; do mogrify -resize 2048x2048 $f; done
