#!/bin/bash

mkdir -p ./vis_overlay

ratio_w=16
ratio_h=10

figsim='vis_tohoku/tohoku'
figres='vis_resources/res'
figtar='vis_overlay/tohoku_res'


# simulation image is the base image
fsim=${figsim}'.0000.png'
w=$(identify -format "%w" ${fsim})
h=$(identify -format "%h" ${fsim})

# desired height
hh=$(($w * $ratio_h))
hh=$(($hh / $ratio_w))
if [[ $(($hh % 2)) != 0 ]]; then
	hh=$(($hh - 1))
fi

# create a white canvas
convert -size ${w}x${hh} xc:white canvas.png

# generate overlay frames
for n in $(seq 0 120);
do
	i=$(printf %04d $n)
	fsim=${figsim}'.'${i}'.png'
	fres=${figres}'.'${i}'.png'
	ftar=${figtar}'.'${i}'.png'

	# side by side
	#convert $figres $figsim +append $target

	# top down
	#convert $figres $figsim -append $target

	# overlay
#	convert ${figsim} -background white -gravity center -extent ${w}x${h} canvas.png 
	convert -gravity north -composite canvas.png ${fsim} -geometry ${w}x${h}+0+100 -depth 8 tmp.png
	convert -gravity southeast -composite tmp.png ${fres} -geometry 1200x600-100+30 -depth 8 ${ftar}
done

# delete tmp files
rm canvas.png
rm tmp.png

# make video
ffmpeg -f image2 -r 4 -s ${w}x${hh} -i ${figtar}.%04d.png -vcodec libx264 -crf 20 -pix_fmt yuv420p demo.mp4

