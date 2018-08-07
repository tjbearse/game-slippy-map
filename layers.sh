X=3
Y=3
Z=1
for z in $(seq 0 $Z); do
    mkdir -p "layers/${z}"
    for x in $(seq -$X $X); do
	for y in $(seq -$Y $Y); do
	    cp tile.png "layers/${z}/${x}.${y}.png"
	done
    done
    (cd layers && mogrify -font Liberation-Sans -fill white -undercolor '#00000080' \
	-pointsize 18 -gravity NorthEast -annotate +10+10 "%d %f" "$z/*.png")
done
