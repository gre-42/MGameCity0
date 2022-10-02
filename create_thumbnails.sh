#!/bin/bash -eux

cd "$(dirname "${BASH_SOURCE[0]}")"

cd split_0

for f in *.obj; do
    render_obj_file "$f" --scale 0.3 --blend_mode continuous --no_shadows --look_at_aabb --output /tmp/out.png
    convert /tmp/out.png -trim -transparent 'rgb(255,0,255)' -resize '50%' "${f%%.obj}_thumb.png"
    rm /tmp/out.png
done;
