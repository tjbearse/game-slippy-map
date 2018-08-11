import unittest
from unittest.mock import patch, call
import numpy as np
import tileMap


class TestScaleRelativeToGlobal(unittest.TestCase):
    def test_zoomZeroEven(self):
        topLeft = np.array([256, 512])
        tileOffset, inTileOffsetPx = tileMap.scaleRelativeToGlobal(topLeft, 0)
        np.testing.assert_array_equal(tileOffset, np.array([1,2]), "tile offset")
        np.testing.assert_array_equal(inTileOffsetPx, np.array([0,0]), "px offset")

    def test_zoomZeroRound(self):
        topLeft = np.array([257, 520])
        tileOffset, inTileOffsetPx = tileMap.scaleRelativeToGlobal(topLeft, 0)
        np.testing.assert_array_equal(tileOffset, np.array([1,2]), "tile offset")
        np.testing.assert_array_equal(inTileOffsetPx, np.array([1,8]), "px offset")

    def test_zoomZeroNegativeEven(self):
        topLeft = np.array([-256, -512])
        tileOffset, inTileOffsetPx = tileMap.scaleRelativeToGlobal(topLeft, 0)
        np.testing.assert_array_equal(tileOffset, np.array([-1,-2]), "tile offset")
        np.testing.assert_array_equal(inTileOffsetPx, np.array([0,0]), "px offset")

    def test_zoomZeroNegativeRound(self):
        topLeft = np.array([-257, -511])
        tileOffset, inTileOffsetPx = tileMap.scaleRelativeToGlobal(topLeft, 0)
        np.testing.assert_array_equal(tileOffset, np.array([-2,-2]), "tile offset")
        np.testing.assert_array_equal(inTileOffsetPx, np.array([255,1]), "px offset")

    def test_zoomOneEven(self):
        topLeft = np.array([256, 512])
        tileOffset, inTileOffsetPx = tileMap.scaleRelativeToGlobal(topLeft, 1)
        np.testing.assert_array_equal(tileOffset, np.array([2,4]), "tile offset")
        np.testing.assert_array_equal(inTileOffsetPx, np.array([0,0]), "px offset")

    def test_zoomOneRound(self):
        topLeft = np.array([257, 520])
        tileOffset, inTileOffsetPx = tileMap.scaleRelativeToGlobal(topLeft, 1)
        np.testing.assert_array_equal(tileOffset, np.array([2,4]), "tile offset")
        np.testing.assert_array_equal(inTileOffsetPx, np.array([2,16]), "px offset")

    def test_zoomOneNegativeEven(self):
        topLeft = np.array([-256, -512])
        tileOffset, inTileOffsetPx = tileMap.scaleRelativeToGlobal(topLeft, 1)
        np.testing.assert_array_equal(tileOffset, np.array([-2,-4]), "tile offset")
        np.testing.assert_array_equal(inTileOffsetPx, np.array([0,0]), "px offset")

    def test_zoomOneNegativeRound(self):
        topLeft = np.array([-257, -511])
        tileOffset, inTileOffsetPx = tileMap.scaleRelativeToGlobal(topLeft, 1)
        np.testing.assert_array_equal(tileOffset, np.array([-3,-4]), "tile offset")
        np.testing.assert_array_equal(inTileOffsetPx, np.array([254,2]), "px offset")

class TestCalcCropParams(unittest.TestCase):
    def test_scale1_noprescale_even(self):
        size = np.array([256, 512])
        pxOffset = np.array([0, 0])
        scale = 1
        #
        prescaleSize, tileSizeToImage, tileDim = tileMap.calcCropParams(size, pxOffset, scale)
        #
        self.assertEqual(tileSizeToImage, 256)
        np.testing.assert_array_equal(prescaleSize, np.array([256,512]), "prescaleSize")
        np.testing.assert_array_equal(tileDim, np.array([1,2]), "tileDim")

    def test_scale1_prescale_even(self):
        size = np.array([250, 500])
        pxOffset = np.array([6, 12])
        scale = 1
        #
        prescaleSize, tileSizeToImage, tileDim = tileMap.calcCropParams(size, pxOffset, scale)
        #
        self.assertEqual(tileSizeToImage, 256)
        np.testing.assert_array_equal(prescaleSize, np.array([256,512]), "prescaleSize")
        np.testing.assert_array_equal(tileDim, np.array([1,2]), "tileDim")

    def test_scale1_prescale_odd(self):
        size = np.array([256, 512])
        pxOffset = np.array([10, 20])
        scale = 1
        #
        prescaleSize, tileSizeToImage, tileDim = tileMap.calcCropParams(size, pxOffset, scale)
        #
        self.assertEqual(tileSizeToImage, 256)
        np.testing.assert_array_equal(prescaleSize, np.array([266,532]), "prescaleSize")
        np.testing.assert_array_equal(tileDim, np.array([2,3]), "tileDim")

    def test_scale2_noprescale_even(self):
        size = np.array([512, 1024])
        pxOffset = np.array([0, 0])
        scale = 2
        #
        prescaleSize, tileSizeToImage, tileDim = tileMap.calcCropParams(size, pxOffset, scale)
        #
        self.assertEqual(tileSizeToImage, 512)
        np.testing.assert_array_equal(prescaleSize, np.array([512,1024]), "prescaleSize")
        np.testing.assert_array_equal(tileDim, np.array([1,2]), "tileDim")

    def test_scale2_prescale_even(self):
        size = np.array([500, 1000])
        pxOffset = np.array([6, 12])
        scale = 2
        #
        prescaleSize, tileSizeToImage, tileDim = tileMap.calcCropParams(size, pxOffset, scale)
        #
        self.assertEqual(tileSizeToImage, 512)
        np.testing.assert_array_equal(prescaleSize, np.array([512,1024]), "prescaleSize")
        np.testing.assert_array_equal(tileDim, np.array([1,2]), "tileDim")

    def test_scale2_prescale_odd(self):
        size = np.array([512, 1024])
        pxOffset = np.array([10, 20])
        scale = 2
        #
        prescaleSize, tileSizeToImage, tileDim = tileMap.calcCropParams(size, pxOffset, scale)
        #
        self.assertEqual(tileSizeToImage, 512)
        np.testing.assert_array_equal(prescaleSize, np.array([532,1064]), "prescaleSize")
        np.testing.assert_array_equal(tileDim, np.array([2,3]), "tileDim")

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
        self.assertEqual(l, [0,1,2])

    def test_neg1to2(self):
        l = list(tileMap.getZooms(2, 4))
        self.assertEqual(l, [-1, 0,1,2])



class TestCrop(unittest.TestCase):
    @patch('tileMap.subprocess.check_call')
    def test_argumentTranslation(self, check_call):
        img = 'fakeimg.png'
        outImg = 'temp/zoom2-%d.png'
        background = tileMap.FillBackground
        preSize = np.array([512,513])
        tileMap.crop(img, outImg, preSize, 256)
        check_call.assert_called_with([
            'convert', img,
            # pre-extend for in-tile offset
            '-background', background,
            '-compose', 'Copy',
            '-gravity', 'SouthEast',
            '-extent', '512x513',
            # crop to tile content in final tile
            '+gravity', '-crop', '256x256',
            # resample large tiles to reg tile size
            '-resize', '256x256',
            # extend partials to full tile size
            '-background', background,
            '-compose', 'Copy',
            '-gravity', 'NorthWest',
            '-extent', '256x256',
            outImg
        ])

class TestMoveToDirs(unittest.TestCase):
    @patch('tileMap.os')
    def test_makeDir(self, mockOs):
        dim = np.array([1, 1])
        offset = np.array([0, 0])
        mockOs.path.exists.return_value = False
        tileMap.moveToDirs(dim, offset, 2)
        mockOs.path.exists.assert_called_with('layers/2')
        mockOs.makedirs.assert_called_with('layers/2')

    @patch('tileMap.os')
    def test_one_noOffset(self, mockOs):
        dim = np.array([1, 1])
        offset = np.array([0, 0])
        mockOs.path.exists.return_value = True
        tileMap.moveToDirs(dim, offset, 0)
        mockOs.rename.assert_has_calls([
            call('temp/zoom0-0.png', 'layers/0/0.0.png'),
        ], any_order=True)

    @patch('tileMap.os')
    def test_oneLine_noOffset(self, mockOs):
        dim = np.array([1, 3])
        offset = np.array([0, 0])
        mockOs.path.exists.return_value = True
        tileMap.moveToDirs(dim, offset, 0)
        mockOs.rename.assert_has_calls([
            call('temp/zoom0-0.png', 'layers/0/0.0.png'),
            call('temp/zoom0-1.png', 'layers/0/0.1.png'),
            call('temp/zoom0-2.png', 'layers/0/0.2.png'),
        ], any_order=True)

    @patch('tileMap.os')
    def test_sixLine_noOffset(self, mockOs):
        dim = np.array([3, 2])
        offset = np.array([0, 0])
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
        dim = np.array([1, 1])
        offset = np.array([1, 2])
        mockOs.path.exists.return_value = True
        tileMap.moveToDirs(dim, offset, 0)
        mockOs.rename.assert_has_calls([
            call('temp/zoom0-0.png', 'layers/0/1.2.png'),
        ], any_order=True)

    @patch('tileMap.os')
    def test_one_NegOffset(self, mockOs):
        dim = np.array([1, 1])
        offset = np.array([-1, 2])
        mockOs.path.exists.return_value = True
        tileMap.moveToDirs(dim, offset, 0)
        mockOs.rename.assert_has_calls([
            call('temp/zoom0-0.png', 'layers/0/-1.2.png'),
        ], any_order=True)

    @patch('tileMap.os')
    def test_one_offsetCrossZero(self, mockOs):
        dim = np.array([2, 2])
        offset = np.array([-1, -1])
        mockOs.path.exists.return_value = True
        tileMap.moveToDirs(dim, offset, 0)
        mockOs.rename.assert_has_calls([
            call('temp/zoom0-0.png', 'layers/0/-1.-1.png'),
            call('temp/zoom0-1.png', 'layers/0/0.-1.png'),
            call('temp/zoom0-2.png', 'layers/0/-1.0.png'),
            call('temp/zoom0-3.png', 'layers/0/0.0.png'),
        ], any_order=True)

if __name__ == '__main__':
    unittest.main()
