#!/usr/bin/env python3
import json
import math
import os
import subprocess
import sys

TileSize=256

config = {
    "zoom": {
        # This is our current scale.
        # Consider
        #   - offset zooms from zero to leave room above? Maybe not an issue if config is nice
        #   - reconfigure numbers to increase the size of the coordinate space (make zero < 1:1). This would make it coordinates on lower layers less fractional.
        # zoom: scale # tile width ft
        -1: 2**(-2),  # 512k  (hexMap native)
        0: 1,         # 256k  (hexMap) move to native?
        1: 2**2,      # 128k  (hexMap) move to native?
        2: 2**(2*2),  # 64k   (hexMap original)
        3: 2**(2*3),  # 16k   (hexMap native)

        # 4: 2**(2*4),# 8k  
        # 5: 2**(2*5),# 2k
        # 6: 2**(2*6),# 500
        # 7: 2**(2*7),# 125
    },
}
# TODO:
#   - Add offset functionality
def main():
    config = readConfig()
    if not os.path.exists("temp"):
        os.makedirs("temp")
    for f, v in config['maps'].items():
        size = v['size']
        baseZoom = v['baseZoom']
        zoomLevels = v['zoomLevels']

        nX, nY = getTileCount(TileSize, size)
        for z in getZooms(baseZoom, zoomLevels):
            s = getRelativeScale(z, baseZoom)
            crop(f, s, z)
            n, w, h = scaleWidthHeight(nX, nY, s)
            moveToDirs(n, w, z)

def getTileCount(tileSize, picSize):
    x = max(math.ceil(picSize[0] / float(tileSize)), 1)
    y = max(math.ceil(picSize[1] / float(tileSize)), 1)
    return x, y

def getRelativeScale(z, baseZoom):
    p = baseZoom - z
    return 2**(p)

def getZooms(base, n):
    return range(base-n+1, base+1)

def scaleWidthHeight(widthN, heightN, s):
    w=max(math.ceil(widthN/s), 1)
    h=max(math.ceil(heightN/s), 1)
    n=w*h
    return n,w,h

def crop(img, s, zoom):
    f = "temp/zoom{}-%d.png".format(zoom)
    w=s*256
    crop="{}x{}".format(w,w)
    subprocess.check_call([
        "convert", img, "+gravity",
        "-crop", crop,
        "-resize", "256x256",
        "-background", "rgba(0,0,0,0)",
        "-compose", "Copy",
        "-gravity", "NorthWest",
        "-extent", "256x256",
        f
    ])

def moveToDirs(N, w, z):
    zdir = "layers/{}".format(z)
    if not os.path.exists(zdir):
        os.makedirs(zdir)
    for n in range(N):
        y=int(n/w)
        x=int(n%w)
        fin = "temp/zoom{}-{}.png".format(z, n)
        fout = "{}/{}.{}.png".format(zdir,x,y)
        os.rename(fin, fout)

def readConfig():
    f = sys.argv[1]
    with open(f, 'r') as fp:
        return json.load(fp)
    

if __name__=="__main__":
    main()
