#!/bin/bash -eux

cd "$(dirname "${BASH_SOURCE[0]}")"

cd textures

for f in *.jpeg; do mogrify -resize 1024x1024 $f; done
