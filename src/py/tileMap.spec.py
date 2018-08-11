import unittest
from unittest.mock import patch, call
import tileMap

class TestGetTileCount(unittest.TestCase):
    def test_even(self):
        x,y = tileMap.getTileCount(10, (20, 30))
        self.assertEqual(x, 2)
        self.assertEqual(y, 3)

    def test_fraction(self):
        x,y = tileMap.getTileCount(10, (5, 4))
        self.assertEqual(x, 1)
        self.assertEqual(y, 1)

    def test_rounding(self):
        x,y = tileMap.getTileCount(10, (15, 24))
        self.assertEqual(x, 2)
        self.assertEqual(y, 3)

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

class TestScaleWidthHeight(unittest.TestCase):
    def test_noScale(self):
        n, w, h = tileMap.scaleWidthHeight(2, 3, 1)
        self.assertEqual(w, 2)
        self.assertEqual(h, 3)
        self.assertEqual(n, 6)

    def test_twoScale(self):
        n, w, h = tileMap.scaleWidthHeight(2, 4, 2)
        self.assertEqual(w, 1)
        self.assertEqual(h, 2)
        self.assertEqual(n, 2)

    def test_intDivision(self):
        n, w, h = tileMap.scaleWidthHeight(3, 3, 2)
        self.assertEqual(w, 2)
        self.assertEqual(h, 2)
        self.assertEqual(n, 4)

    def test_bigScale(self):
        n, w, h = tileMap.scaleWidthHeight(3, 3, 64)
        self.assertEqual(w, 1)
        self.assertEqual(h, 1)
        self.assertEqual(n, 1)

    def test_fractionalScale(self):
        n, w, h = tileMap.scaleWidthHeight(3, 3, .5)
        self.assertEqual(w, 6)
        self.assertEqual(h, 6)
        self.assertEqual(n, 36)

class TestCropBaseTest(unittest.TestCase):
    @patch('tileMap.subprocess.check_call')
    def test_noScale(self, check_call):
        img = 'fakeimg.png'
        tileMap.crop(img, 1, 2)
        check_call.assert_called_with([
            'convert', img, '+gravity',
            '-crop', '256x256',
            '-resize', '256x256',
            '-background', 'rgba(0,0,0,0)',
            '-compose', 'Copy',
            '-gravity', 'NorthWest',
            '-extent', '256x256',
            'temp/zoom2-%d.png'
        ])

    @patch('tileMap.subprocess.check_call')
    def test_scale2(self, check_call):
        img = 'fakeimg.png'
        tileMap.crop(img, 2, 2)
        check_call.assert_called_with([
            'convert', img, '+gravity',
            '-crop', '512x512',
            '-resize', '256x256',
            '-background', 'rgba(0,0,0,0)',
            '-compose', 'Copy',
            '-gravity', 'NorthWest',
            '-extent', '256x256',
            'temp/zoom2-%d.png'
        ])

class TestMoveToDirs(unittest.TestCase):
    @patch('tileMap.os')
    def test_makeDir(self, mockOs):
        mockOs.path.exists.return_value = False
        tileMap.moveToDirs(1, 1, 2)
        mockOs.path.exists.assert_called_with('layers/2')
        mockOs.makedirs.assert_called_with('layers/2')

    @patch('tileMap.os')
    def test_one(self, mockOs):
        mockOs.path.exists.return_value = True
        tileMap.moveToDirs(1, 1, 0)
        mockOs.rename.has_calls([
            call('temp/zoom0-1.png', '0/1.0.png'),
        ], any_order=True)

    @patch('tileMap.os')
    def test_oneLine(self, mockOs):
        mockOs.path.exists.return_value = True
        tileMap.moveToDirs(3, 1, 0)
        mockOs.rename.assert_has_calls([
            call('temp/zoom0-0.png', 'layers/0/0.0.png'),
            call('temp/zoom0-1.png', 'layers/0/0.1.png'),
            call('temp/zoom0-2.png', 'layers/0/0.2.png'),
        ], any_order=True)

    @patch('tileMap.os')
    def test_sixLine(self, mockOs):
        mockOs.path.exists.return_value = True
        tileMap.moveToDirs(6, 3, 0)
        mockOs.rename.assert_has_calls([
            call('temp/zoom0-0.png', 'layers/0/0.0.png'),
            call('temp/zoom0-1.png', 'layers/0/1.0.png'),
            call('temp/zoom0-2.png', 'layers/0/2.0.png'),
            call('temp/zoom0-3.png', 'layers/0/0.1.png'),
            call('temp/zoom0-4.png', 'layers/0/1.1.png'),
            call('temp/zoom0-5.png', 'layers/0/2.1.png')
        ], any_order=True)

if __name__ == '__main__':
    unittest.main()
