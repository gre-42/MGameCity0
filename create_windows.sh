#!/bin/bash -eux

cd "$(dirname "${BASH_SOURCE[0]}")"

cd split_0

for f in *.obj; do
    render_obj_file "$f" --scale 5 --blend_mode continuous --no_shadows --output /tmp/out.png
    convert /tmp/out.png -trim -transparent 'rgb(255,0,255)' /tmp/"${f%%.obj}_windows.png"
    rm /tmp/out.png
done;
