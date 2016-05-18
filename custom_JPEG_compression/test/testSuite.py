import unittest
import os

from custom_JPEG_compression.imgUtils import CompressionCore

STANDARD_JPEG_BLOCK_SIZE = 8 

class Test(unittest.TestCase):

    def testOpenImage(self):
        compressionCore = CompressionCore()
        compressionCore.openImage(os.path.join(os.path.dirname(__file__), "./images/test.bmp"))
        return compressionCore

    def testGetPixel(self):
        compressionCore = self.testOpenImage()
        compressionCore.getImagePixel()
        assert (len(compressionCore.originalImagePixels) == compressionCore.originalImageHeight)
        assert (len(compressionCore.originalImagePixels[0]) == compressionCore.originalImageWidth)
        return compressionCore

    def testImageSquaring(self):
        compressionCore = self.testGetPixel()
        for index in [-1, 0, 1, 2, 3, 10, 50, 100, 150, 200, 500]:
            compressionCore.imageSquaring(index)
            assert (compressionCore.squareImageHeight % STANDARD_JPEG_BLOCK_SIZE * index == 0)
            assert (compressionCore.squareImageWidth % STANDARD_JPEG_BLOCK_SIZE * index == 0)

if __name__ == "__main__":
    unittest.main()
