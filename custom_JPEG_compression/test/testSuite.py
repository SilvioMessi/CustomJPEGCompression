import unittest
import os
import numpy as np

from custom_JPEG_compression.imgUtils import CompressionCore

STANDARD_JPEG_BLOCK_SIZE = 8
TEST_SEPARATOR = "--------------------------------------------" 

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
        pixelsMatrix = np.asarray([[ 231 , 32, 233, 161, 24, 71, 140, 245],
                                    [247, 40, 248, 245, 124, 204, 36, 107],
                                    [234, 202, 245, 167, 9, 217, 239, 173],
                                    [193, 190, 100, 167, 43, 180, 8, 70],
                                    [ 11, 24, 210, 177, 81, 243, 8, 112],
                                    [ 97, 195, 203, 47, 125, 114, 165, 181],
                                    [193, 70, 174, 167, 41, 30, 127, 245],
                                    [ 87, 149, 57, 192, 65, 129, 178, 228]])
        compressionCore = CompressionCore()
        np.set_printoptions(precision=3, linewidth=200)
        print ("DTC1 TEST")
        print (pixelsMatrix[1,:])
        print (compressionCore.DCT1(pixelsMatrix[1,:]))
        print (TEST_SEPARATOR)
        print ("DTC2 TEST")
        print (pixelsMatrix)
        print (compressionCore.DCT2(pixelsMatrix))
        print (TEST_SEPARATOR)
    
    def testQuantizationMatrix(self):
        quality80QuantizationMatrix = np.asarray ([[6, 4, 4, 6, 10, 16, 20, 24],
                                                    [5, 5, 6, 8, 10, 23, 24, 22],
                                                    [6, 5, 6, 10, 16, 23, 28, 22],
                                                    [6, 7, 9, 12, 20, 35, 32, 25],
                                                    [7, 9, 15, 22, 27, 44, 41, 31],
                                                    [10, 14, 22, 26, 32, 42, 45, 37],
                                                    [20, 26, 31, 35, 41, 48, 48, 40],
                                                    [29, 37, 38, 39, 45, 40, 41, 40]])
        compressionCore = CompressionCore()
        quantizationMatrix = compressionCore.compute8X8QuantizationMaxtrix(80)
        assert (np.array_equal(quality80QuantizationMatrix, quantizationMatrix) == True)
        print ("8x8 QUANTIZATION MATRIX")
        print (quantizationMatrix)
        print (TEST_SEPARATOR)
        print ("8Nx8N QUANTIZATION MATRIX (N=2)")
        compressionCore.blockSizeMoltiplicator = 2
        print (compressionCore.compute8NX8NQuantizationMaxtrix(80))

if __name__ == "__main__":
    unittest.main()
