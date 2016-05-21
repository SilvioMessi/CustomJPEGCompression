import unittest
import os

from custom_JPEG_compression.imgUtils import CompressionCore

STANDARD_JPEG_BLOCK_SIZE = 8 

class Test(unittest.TestCase):

    def testOpenImageAndGetPixels(self):
        compressionCore = CompressionCore()
        compressionCore.openImage(os.path.join(os.path.dirname(__file__), "./images/test.bmp"))
        assert (len(compressionCore.originalImagePixels) == compressionCore.originalImageHeight)
        assert (len(compressionCore.originalImagePixels[0]) == compressionCore.originalImageWidth)
        return compressionCore

    def testImageSquaring(self):
        compressionCore = self.testOpenImageAndGetPixels()
        for index in [-1, 0, 1, 2, 3, 10, 50, 100, 150, 200, 500]:
            compressionCore.imageSquaring(index)
            assert (compressionCore.squareImageHeight % STANDARD_JPEG_BLOCK_SIZE * index == 0)
            assert (compressionCore.squareImageWidth % STANDARD_JPEG_BLOCK_SIZE * index == 0)

    def testDTC(self):
        pixelsMatrix = [[ 231 , 32, 233, 161, 24, 71, 140, 245],
        [247, 40, 248, 245, 124, 204, 36, 107],
        [234, 202, 245, 167, 9, 217, 239, 173],
        [193, 190, 100, 167, 43, 180, 8, 70],
        [ 11, 24, 210, 177, 81, 243, 8, 112],
        [ 97, 195, 203, 47, 125, 114, 165, 181],
        [193, 70, 174, 167, 41, 30, 127, 245],
        [ 87, 149, 57, 192, 65, 129, 178, 228]]
        compressionCore = CompressionCore()
        print ("DTC1 TEST")
        print (pixelsMatrix[0])
        tmp = compressionCore.DCT1(pixelsMatrix[0])
        print (tmp)
        print ("DTC2 TEST")
        print (pixelsMatrix)
        tmp = compressionCore.DCT2(pixelsMatrix)
        print (tmp)

if __name__ == "__main__":
    unittest.main()
