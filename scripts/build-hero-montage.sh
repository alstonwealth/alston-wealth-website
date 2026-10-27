#!/bin/bash
# Hero montage, two versions from the same five scenes:
#   desktop  1280x720, full frame
#   mobile    405x720, each scene cropped to its own subject (MOBX = left edge of the crop).
#             "fit" shows the whole frame at phone width over a blurred copy of itself, for
#             scenes whose subjects are too far apart to crop (the porch couple).
# Order: office -> meeting table -> porch -> father and son -> handshake (last, by request).
# 4 s per scene, 0.8 s crossfades, seamless loop (16.0 s).
# Usage: scripts/build-hero-montage.sh <out_dir>     (run from the alston/ folder)
set -e
IN=source-video; OUT=${1:-/tmp/montage}; mkdir -p "$OUT"
X=0.8; L=4
#        file                 start  mobile-crop-x
SCENES=("scene-office         1.0    760"
        "scene-porch          5.2    fit"
        "scene-father-son     1.0    470"
        "scene-meeting-table  0.3    640"
        "scene-handshake      1.0    330")
build () {  # $1 = desktop|mobile
  local args=() fc="" i=0 n=${#SCENES[@]}
  for s in "${SCENES[@]}" "${SCENES[0]}"; do
    read f st mx <<<"$s"
    local len=$L; [ $i -eq $n ] && len=$X
    args+=(-ss $st -t $len -i $IN/$f.mp4)
    local pre="[$i:v]"
    if [ "$1" = mobile ] && [ "$mx" = fit ]; then
      fc+="[$i:v]split=2[bg$i][fg$i];[bg$i]crop=404:720:440:0,gblur=sigma=24,eq=brightness=-0.12[bgb$i];[fg$i]crop=1060:720:110:0,scale=404:-2,format=rgba,geq=r='r(X,Y)':g='g(X,Y)':b='b(X,Y)':a='255*min(1,min(Y,H-1-Y)/36)'[fgs$i];[bgb$i][fgs$i]overlay=0:(H-h)/2+40:format=auto,format=yuv420p[c$i];"
      pre="[c$i]"; crop=""
    elif [ "$1" = mobile ]; then crop="crop=404:720:$mx:0,"; else crop=""; fi
    fc+="${pre}${crop}setsar=1,fps=24,eq=saturation=0.88:contrast=1.02,format=yuv420p,setpts=PTS-STARTPTS[s$i];"
    i=$((i+1))
  done
  local prev=s0 off
  for j in $(seq 1 $n); do
    off=$(python3 -c "print(round($j*($L-$X),3))")
    fc+="[$prev][s$j]xfade=transition=fade:duration=$X:offset=$off[x$j];"; prev=x$j
  done
  fc+="[$prev]trim=start=$X,setpts=PTS-STARTPTS[v]"
  ffmpeg -v error -y "${args[@]}" -filter_complex "$fc" -map "[v]" -an -c:v libx264 -preset slow -crf 17 -pix_fmt yuv420p "$OUT/master-$1.mp4"
}
build desktop
build mobile
M=src/media
for v in desktop mobile; do
  suf=$([ $v = desktop ] && echo "" || echo "-mobile")
  ffmpeg -v error -y -i "$OUT/master-$v.mp4" -an -c:v libx264 -preset slow -crf $([ $v = desktop ] && echo 25 || echo 23) -profile:v high -pix_fmt yuv420p -movflags +faststart $M/hero-montage$suf.mp4
  ffmpeg -v error -y -i "$OUT/master-$v.mp4" -an -c:v libvpx-vp9 -b:v 0 -crf $([ $v = desktop ] && echo 35 || echo 33) -row-mt 1 -deadline good -cpu-used 2 $M/hero-montage$suf.webm
  ffmpeg -v error -y -ss 1.5 -i "$OUT/master-$v.mp4" -frames:v 1 -q:v 3 $M/hero-poster$suf.jpg
done
