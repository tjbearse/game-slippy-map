#!/usr/bin/env python3
import json
import math
import os
import subprocess
import sys

TileSize=256
FillBackground='rgba(0,0,0,0)'

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

"""
config details:
    size:	w,h of the image in pixels
    baseZoom:	most zoomed level the image will be tiled to
    zoomLevels: number of zoom levels to count up from base (includes base)
    topLeft:	global coordinate of the top left corner of the image
"""

def main():
    config = readConfig()
    if not os.path.exists("temp"):
        os.makedirs("temp")

    layerSettings = []
    for f, v in config['maps'].items():
        size = v['size']
        baseZoom = v['baseZoom']
        zoomLevels = v['zoomLevels']
        topLeft = mapCoordToImgCoord(v['topLeft'])

        bounds = setBounding(size, topLeft, baseZoom)
        zoomRange = getZooms(baseZoom, zoomLevels)
        layerSettings.append(organizeLayerSettings(bounds, zoomRange))
        for z in range(zoomRange[0], zoomRange[1]+1):
            tileOffset, inTileOffsetPx = scaleRelativeToGlobal(topLeft, z)

            scaleRelativeToImage = getRelativeScale(z, baseZoom)
            resize, rescaleTile, tileDim = calcCropParams(size, inTileOffsetPx, scaleRelativeToImage)
            print("z:{}, n:{}, o:{}".format(z, tileDim, tileOffset))

            imgOut = "temp/zoom{}-%d.png".format(z)
            crop(f, imgOut, resize, rescaleTile)
            moveToDirs(tileDim, tileOffset, z)
    saveLayerSettings("layers/layers.js", layerSettings)

def saveLayerSettings(fname, layers):
    js = 'var layers = {};'.format(json.dumps(layers))
    with open(fname, 'w') as f:
        f.write(js)

def organizeLayerSettings(bounds, zoomRange):
    return {
        'bounds': bounds,
        'minZoom': zoomRange[0],
        'maxZoom': zoomRange[1],
    }

def setBounding(size, topLeft, zoom):
    s = float(getGlobalScale(zoom))
    bottomRight = [
        (size[0] / s) + topLeft[0],
        (size[1] / s) + topLeft[1],
    ]
    return lmap(imgCoordToMapCoord, [topLeft, bottomRight])

# map is LatLng, imgs are x,y with y increasing as it goes down
def mapCoordToImgCoord(coord):
    return [coord[1], -coord[0]]
def imgCoordToMapCoord(coord):
    return [-coord[1], coord[0]]

def scaleRelativeToGlobal(globalOffet, z):
    # rel to layer pixels after tiling (256 size)
    scaleRelativeToGlobal = getGlobalScale(z)
    layerOffsetPx = lmap(lambda x:x * scaleRelativeToGlobal, globalOffet)
    tileOffset = lmap(lambda x:math.floor(x / TileSize), layerOffsetPx)
    inTileOffsetPx = lmap(lambda x:x % TileSize, layerOffsetPx)
    return tileOffset, inTileOffsetPx

# this number times a global coordinate should give a pixel coordinate
def getGlobalScale(zoom):
    return 2.0**(zoom)

def calcCropParams(size, inTileOffsetPx, scaleRelativeToImage):
    topLeftExtraToImage = lmap(lambda x:x * scaleRelativeToImage, inTileOffsetPx)
    prescaleSize = lmap(sum, zip(size, topLeftExtraToImage))
    tileSizeToImage = 256 * scaleRelativeToImage
    tileDim = lmap(lambda x:math.ceil(x/tileSizeToImage), prescaleSize)
    return prescaleSize, tileSizeToImage, tileDim

def getRelativeScale(z, baseZoom):
    return getGlobalScale(baseZoom) / getGlobalScale(z)

def getZooms(base, n):
    return [base-n+1, base]

def crop(imgIn, imgOut, prescaleSize, tileSizeToImage):
    preSize="{}x{}".format(*prescaleSize)
    crop="{0}x{0}".format(tileSizeToImage)
    tileSize="{0}x{0}".format(TileSize)
    subprocess.check_call([
        'convert', imgIn,
        # pre-extend for in-tile offset
        '-background', FillBackground,
        '-compose', 'Copy',
        '-gravity', 'SouthEast',
        '-extent', preSize,
        # crop to tile content in final tile
        '+gravity', '-crop', crop,
        # extend partials to full crop size
        '-background', FillBackground,
        '-compose', 'Copy',
        '-gravity', 'NorthWest',
        '-extent', crop,
        # resample large tiles to reg tile size
        '-resize', tileSize,
        imgOut
    ])

def moveToDirs(dim, offset, z):
    w,h = int(dim[0]), int(dim[1])
    xOffset, yOffset = int(offset[0]), int(offset[1])
    zdir = "layers/{}".format(z)
    if not os.path.exists(zdir):
        os.makedirs(zdir)
    for n in range(w*h):
        y=int(n/w) + yOffset
        x=int(n%w) + xOffset
        fin = "temp/zoom{}-{}.png".format(z, n)
        fout = "{}/{}.{}.png".format(zdir,x,y)
        os.rename(fin, fout)

def lmap(*arg):
    return list(map(*arg))

def readConfig():
    f = sys.argv[1]
    with open(f, 'r') as fp:
        return json.load(fp)

if __name__=="__main__":
    main()
