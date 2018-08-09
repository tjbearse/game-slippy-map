#!/usr/bin/env python2
from subprocess import check_call
import os

# zoom1svg='mapParts/zoom1-0.0-16x16.svg'
# should be 4096x4096
# TODO make zoom1 from svg if not exists (do this in make instead?

TileSize=256

def main():
    hexMap = 'mapParts/exports/z2-hexmap-2048x2048.png'
    size = (2048, 2048)
    tileDim = map(lambda x: x/TileSize, size)
    if not os.path.exists("temp"):
        os.makedirs("temp")
    nZoom=3
    for z in range(nZoom):
        w, h = createZoomLevel(hexMap, z, tileDim[0], tileDim[1], nZoom-1-z)
        if z==0:
            print "bounds: [[-{}*{}, 0], [0, {}*{}]],".format(w, TileSize, h, TileSize)

# TODO allow offsets
def createZoomLevel(img, zoom, widthN, heightN, scale=0):
    print "zoom{}@{}".format(zoom, scale)
    f = "temp/zoom{}-%d.png".format(zoom)
    s=2**(scale)
    if scale == 0:
        check_call(["convert", img, "+gravity", "-crop", "256x256", f])
    else:
        w=s*256
        crop="{}x{}".format(w,w)
        check_call(["convert", img, "+gravity",
                    "-crop", crop,
                    "-resize", "256x256",
                f])
    # assumes square
    w=widthN/s
    h=heightN/s
    n=w*h
    moveToDirs(n, w, zoom)
    return w,h

"""
# zoom 2
print "zoom2"
check_call(["convert", zoom2, "+gravity", "-crop", "256x256", "temp/zoom2-%d.png"])

# zoom 1
print "zoom1"
check_call(["convert", zoom2, "+gravity", "-crop", "1024x1024", "-resize", "256x256", "temp/zoom1-%d.png"])

# zoom 0
print "zoom0"
check_call(["convert", zoom2, "+gravity", "-crop", "4096x4096", "-resize", "256x256", "temp/zoom0-%d.png"])
"""

# TODO add an offset param
def moveToDirs(N, w, z):
    zdir = "layers/{}".format(z)
    if not os.path.exists(zdir):
        os.makedirs(zdir)
    for n in range(N):
        y=n/w
        x=n%w
        fin = "temp/zoom{}-{}.png".format(z, n)
        fout = "{}/{}.{}.png".format(zdir,x,y)
        os.rename(fin, fout)
main()
