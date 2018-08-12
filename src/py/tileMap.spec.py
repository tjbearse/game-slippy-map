import unittest
from unittest.mock import patch, call
import tileMap


class TestScaleRelativeToGlobal(unittest.TestCase):
    def test_zoomZeroEven(self):
        topLeft = [256, 512]
        tileOffset, inTileOffsetPx = tileMap.scaleRelativeToGlobal(topLeft, 0)
        self.assertEqual(tileOffset, [1,2], "tile offset")
        self.assertEqual(inTileOffsetPx, [0,0], "px offset")

    def test_zoomZeroRound(self):
        topLeft = [257, 520]
        tileOffset, inTileOffsetPx = tileMap.scaleRelativeToGlobal(topLeft, 0)
        self.assertEqual(tileOffset, [1,2], "tile offset")
        self.assertEqual(inTileOffsetPx, [1,8], "px offset")

    def test_zoomZeroNegativeEven(self):
        topLeft = [-256, -512]
        tileOffset, inTileOffsetPx = tileMap.scaleRelativeToGlobal(topLeft, 0)
        self.assertEqual(tileOffset, [-1,-2], "tile offset")
        self.assertEqual(inTileOffsetPx, [0,0], "px offset")

    def test_zoomZeroNegativeRound(self):
        topLeft = [-257, -511]
        tileOffset, inTileOffsetPx = tileMap.scaleRelativeToGlobal(topLeft, 0)
        self.assertEqual(tileOffset, [-2,-2], "tile offset")
        self.assertEqual(inTileOffsetPx, [255,1], "px offset")

    def test_zoomOneEven(self):
        topLeft = [256, 512]
        tileOffset, inTileOffsetPx = tileMap.scaleRelativeToGlobal(topLeft, 1)
        self.assertEqual(tileOffset, [2,4], "tile offset")
        self.assertEqual(inTileOffsetPx, [0,0], "px offset")

    def test_zoomOneRound(self):
        topLeft = [257, 520]
        tileOffset, inTileOffsetPx = tileMap.scaleRelativeToGlobal(topLeft, 1)
        self.assertEqual(tileOffset, [2,4], "tile offset")
        self.assertEqual(inTileOffsetPx, [2,16], "px offset")

    def test_zoomOneNegativeEven(self):
        topLeft = [-256, -512]
        tileOffset, inTileOffsetPx = tileMap.scaleRelativeToGlobal(topLeft, 1)
        self.assertEqual(tileOffset, [-2,-4], "tile offset")
        self.assertEqual(inTileOffsetPx, [0,0], "px offset")

    def test_zoomOneNegativeRound(self):
        topLeft = [-257, -511]
        tileOffset, inTileOffsetPx = tileMap.scaleRelativeToGlobal(topLeft, 1)
        self.assertEqual(tileOffset, [-3,-4], "tile offset")
        self.assertEqual(inTileOffsetPx, [254,2], "px offset")

class TestCalcCropParams(unittest.TestCase):
    def test_scale1_noprescale_even(self):
        size = [256, 512]
        pxOffset = [0, 0]
        scale = 1
        #
        prescaleSize, tileSizeToImage, tileDim = tileMap.calcCropParams(size, pxOffset, scale)
        #
        self.assertEqual(tileSizeToImage, 256)
        self.assertEqual(prescaleSize, [256,512], "prescaleSize")
        self.assertEqual(tileDim, [1,2], "tileDim")

    def test_scale1_prescale_even(self):
        size = [250, 500]
        pxOffset = [6, 12]
        scale = 1
        #
        prescaleSize, tileSizeToImage, tileDim = tileMap.calcCropParams(size, pxOffset, scale)
        #
        self.assertEqual(tileSizeToImage, 256)
        self.assertEqual(prescaleSize, [256,512], "prescaleSize")
        self.assertEqual(tileDim, [1,2], "tileDim")

    def test_scale1_prescale_odd(self):
        size = [256, 512]
        pxOffset = [10, 20]
        scale = 1
        #
        prescaleSize, tileSizeToImage, tileDim = tileMap.calcCropParams(size, pxOffset, scale)
        #
        self.assertEqual(tileSizeToImage, 256)
        self.assertEqual(prescaleSize, [266,532], "prescaleSize")
        self.assertEqual(tileDim, [2,3], "tileDim")

    def test_scale2_noprescale_even(self):
        size = [512, 1024]
        pxOffset = [0, 0]
        scale = 2
        #
        prescaleSize, tileSizeToImage, tileDim = tileMap.calcCropParams(size, pxOffset, scale)
        #
        self.assertEqual(tileSizeToImage, 512)
        self.assertEqual(prescaleSize, [512,1024], "prescaleSize")
        self.assertEqual(tileDim, [1,2], "tileDim")

    def test_scale2_prescale_even(self):
        size = [500, 1000]
        pxOffset = [6, 12]
        scale = 2
        #
        prescaleSize, tileSizeToImage, tileDim = tileMap.calcCropParams(size, pxOffset, scale)
        #
        self.assertEqual(tileSizeToImage, 512)
        self.assertEqual(prescaleSize, [512,1024], "prescaleSize")
        self.assertEqual(tileDim, [1,2], "tileDim")

    def test_scale2_prescale_odd(self):
        size = [512, 1024]
        pxOffset = [10, 20]
        scale = 2
        #
        prescaleSize, tileSizeToImage, tileDim = tileMap.calcCropParams(size, pxOffset, scale)
        #
        self.assertEqual(tileSizeToImage, 512)
        self.assertEqual(prescaleSize, [532,1064], "prescaleSize")
        self.assertEqual(tileDim, [2,3], "tileDim")

class TestGetRelativeScale(unittest.TestCase):
    def test_self(self):
        s = tileMap.getRelativeScale(2, 2)
        self.assertEqual(s, 1)

    def test_selfZero(self):
        s = tileMap.getRelativeScale(0, 0)
        self.assertEqual(s, 1)

    def test_first(self):
        s = tileMap.getRelativeScale(1, 2)
        self.assertEqual(s, 2)

    def test_second(self):
        s = tileMap.getRelativeScale(0, 2)
        self.assertEqual(s, 4)

class TestGetZooms(unittest.TestCase):
    def test_0to2(self):
        l = list(tileMap.getZooms(2, 3))
        self.assertEqual(l, [0,2])

    def test_neg1to2(self):
        l = list(tileMap.getZooms(2, 4))
        self.assertEqual(l, [-1,2])



class TestCrop(unittest.TestCase):
    @patch('tileMap.subprocess.check_call')
    def test_argumentTranslation(self, check_call):
        img = 'fakeimg.png'
        outImg = 'temp/zoom2-%d.png'
        background = tileMap.FillBackground
        preSize = [512,513]
        tileMap.crop(img, outImg, preSize, 1024)
        check_call.assert_called_with([
            'convert', img,
            #
            '-background', background,
            '-compose', 'Copy',
            '-gravity', 'SouthEast',
            '-extent', '512x513',
            #
            '+gravity', '-crop', '1024x1024',
            #
            '-background', background,
            '-compose', 'Copy',
            '-gravity', 'NorthWest',
            '-extent', '1024x1024',
            #
            '-resize', '256x256',
            outImg
        ])

class TestMoveToDirs(unittest.TestCase):
    @patch('tileMap.os')
    def test_makeDir(self, mockOs):
        dim = [1, 1]
        offset = [0, 0]
        mockOs.path.exists.return_value = False
        tileMap.moveToDirs(dim, offset, 2)
        mockOs.path.exists.assert_called_with('layers/2')
        mockOs.makedirs.assert_called_with('layers/2')

    @patch('tileMap.os')
    def test_one_noOffset(self, mockOs):
        dim = [1, 1]
        offset = [0, 0]
        mockOs.path.exists.return_value = True
        tileMap.moveToDirs(dim, offset, 0)
        mockOs.rename.assert_has_calls([
            call('temp/zoom0-0.png', 'layers/0/0.0.png'),
        ], any_order=True)

    @patch('tileMap.os')
    def test_oneLine_noOffset(self, mockOs):
        dim = [1, 3]
        offset = [0, 0]
        mockOs.path.exists.return_value = True
        tileMap.moveToDirs(dim, offset, 0)
        mockOs.rename.assert_has_calls([
            call('temp/zoom0-0.png', 'layers/0/0.0.png'),
            call('temp/zoom0-1.png', 'layers/0/0.1.png'),
            call('temp/zoom0-2.png', 'layers/0/0.2.png'),
        ], any_order=True)

    @patch('tileMap.os')
    def test_sixLine_noOffset(self, mockOs):
        dim = [3, 2]
        offset = [0, 0]
        mockOs.path.exists.return_value = True
        tileMap.moveToDirs(dim, offset, 0)
        mockOs.rename.assert_has_calls([
            call('temp/zoom0-0.png', 'layers/0/0.0.png'),
            call('temp/zoom0-1.png', 'layers/0/1.0.png'),
            call('temp/zoom0-2.png', 'layers/0/2.0.png'),
            call('temp/zoom0-3.png', 'layers/0/0.1.png'),
            call('temp/zoom0-4.png', 'layers/0/1.1.png'),
            call('temp/zoom0-5.png', 'layers/0/2.1.png')
        ], any_order=True)

    @patch('tileMap.os')
    def test_one_PosOffset(self, mockOs):
        dim = [1, 1]
        offset = [1, 2]
        mockOs.path.exists.return_value = True
        tileMap.moveToDirs(dim, offset, 0)
        mockOs.rename.assert_has_calls([
            call('temp/zoom0-0.png', 'layers/0/1.2.png'),
        ], any_order=True)

    @patch('tileMap.os')
    def test_one_NegOffset(self, mockOs):
        dim = [1, 1]
        offset = [-1, 2]
        mockOs.path.exists.return_value = True
        tileMap.moveToDirs(dim, offset, 0)
        mockOs.rename.assert_has_calls([
            call('temp/zoom0-0.png', 'layers/0/-1.2.png'),
        ], any_order=True)

    @patch('tileMap.os')
    def test_one_offsetCrossZero(self, mockOs):
        dim = [2, 2]
        offset = [-1, -1]
        mockOs.path.exists.return_value = True
        tileMap.moveToDirs(dim, offset, 0)
        mockOs.rename.assert_has_calls([
            call('temp/zoom0-0.png', 'layers/0/-1.-1.png'),
            call('temp/zoom0-1.png', 'layers/0/0.-1.png'),
            call('temp/zoom0-2.png', 'layers/0/-1.0.png'),
            call('temp/zoom0-3.png', 'layers/0/0.0.png'),
        ], any_order=True)

class TestSetBounding(unittest.TestCase):
    def test_zoomZero_zero(self):
        topLeft = [0, 0]
        size = [256, 512]
        a, b = tileMap.setBounding(size, topLeft, 0)
        self.assertEqual(a, [0,0], "a")
        self.assertEqual(b, [-512,256], "b")

    def test_zoomZero_pos(self):
        topLeft = [1024, 2048]
        size = [256, 512]
        a, b = tileMap.setBounding(size, topLeft, 0)
        self.assertEqual(a, [-2048,1024], "a")
        self.assertEqual(b, [-2560,1280], "b")

    def test_zoomZero_neg(self):
        topLeft = [-256, -512]
        size = [256, 512]
        a, b = tileMap.setBounding(size, topLeft, 0)
        self.assertEqual(a, [512,-256], "a")
        self.assertEqual(b, [0,0], "b")

    def test_zoom1_zero(self):
        topLeft = [0, 0]
        size = [256, 512]
        a, b = tileMap.setBounding(size, topLeft, 1)
        self.assertEqual(a, [0,0], "a")
        self.assertEqual(b, [-256,128], "b")

    def test_zoom1_pos(self):
        topLeft = [256, 512]
        size = [256, 512]
        a, b = tileMap.setBounding(size, topLeft, 1)
        self.assertEqual(a, [-512,256], "a")
        self.assertEqual(b, [-768,384], "b")

    def test_zoom1_neg(self):
        topLeft = [-256, -512]
        size = [256, 512]
        a, b = tileMap.setBounding(size, topLeft, 1)
        self.assertEqual(a, [512,-256], "a")
        self.assertEqual(b, [256,-128], "b")

if __name__ == '__main__':
    unittest.main()
